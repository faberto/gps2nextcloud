#!/usr/bin/python3
import argparse
import importlib
import logging
import multiprocessing
import selectors
import socket
import traceback
from builtins import KeyboardInterrupt, Exception, RuntimeError, getattr, exit
from multiprocessing import Process

from gps2nextcloud.server_config import get_gate_sections, get_config, create_config, create_daemon

sel = selectors.DefaultSelector()
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
logAllMessages = False


def accept_wrapper(sock, gate_class, protocol_class, cfg, section_name):
    conn, addr = sock.accept()  # Should be ready to read
    logger.info("accepted connection from %s", addr)
    conn.setblocking(False)
    gate = gate_class(cfg, section_name)
    protocol = protocol_class(sel, conn, addr, gate, logAllMessages)
    sel.register(conn, selectors.EVENT_READ, data=protocol)
    return protocol


def server_func(config_path, section_name):
    cfg = get_config(config_path)
    global logAllMessages
    logAllMessages = cfg.get('General', 'logAllMessages') == 'true'
    host = cfg.get(section_name, 'host')
    port = cfg.getint(section_name, 'port')
    gate_type = cfg.get(section_name, 'gate')
    get_type_splits = gate_type.split(':')
    gate_module_name = get_type_splits[0]
    gate_class_name = get_type_splits[1]
    gate_module = importlib.import_module(gate_module_name)
    gate_class = getattr(gate_module, gate_class_name)
    protocol_type = cfg.get(section_name, 'protocol')
    protocol_type_splits = protocol_type.split(':')
    protocol_module_name = protocol_type_splits[0]
    protocol_class_name = protocol_type_splits[1]
    protocol_module = importlib.import_module(protocol_module_name)
    protocol_class = getattr(protocol_module, protocol_class_name)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((host, port))
    listen_socket.listen()
    logger.info('listening on %s:%d', host, port)
    listen_socket.setblocking(False)
    sel.register(listen_socket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    message = accept_wrapper(key.fileobj, gate_class, protocol_class, cfg, section_name)
                    if message:
                        message.process_events(mask)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)

                    except RuntimeError as ex:
                        if ex.__str__() != 'Peer closed.':
                            logger.error( "main: error: exception for s", message.addr,  exc_info=1)
                        else:
                            logger.info("connection closed %s", message.addr)

                    except ConnectionResetError:
                        logger.info("connection reset error %s",  message.addr)
                        message.close()

                    except Exception:
                        errmsg = "main: error: exception "
                        if message.addr:
                            errmsg += message.addr
                        errmsg += "\n"
                        errmsg += traceback.format_exc()
                        logger.exception(errmsg)
                        message.close()
    except KeyboardInterrupt:
        logger.info("caught keyboard interrupt, exiting")
    finally:
        sel.close()


def run(config_path):
    servers = []
    try:
        gate_sections = get_gate_sections(config_path)
        for section in iter(gate_sections):
            server = Process(target=server_func, name=f"gps2nextcloud_{section}", args=(config_path, section,))
            servers.append(server)
            server.start()
        for server in servers:
            server.join()
    except KeyboardInterrupt:
        pass
    finally:
        sel.close()
        for server in servers:
            server.join()


def daemon_run():
    parser = argparse.ArgumentParser("gps2nextcloud")
    parser.add_argument("--create-daemon", help="create systemd service file /etc/systemd/system/gps2nextcloud.service",
                        action='store_true')
    parser.add_argument("--create-config", help="create initial configuration file", action='store_true')
    parser.add_argument("--config_file", help="path to configuration file", required=False)
    args = parser.parse_args()
    if args.config_file:
        run(args.config_file)
    else:
        exit(-5)


def main():
    parser = argparse.ArgumentParser("gps2nextcloud")
    parser.add_argument("--create-daemon", help="create systemd service file /etc/systemd/system/gps2nextcloud.service",
                        action='store_true')
    parser.add_argument("--create-config", help="create initial configuration file", action='store_true')
    parser.add_argument("--config_file", help="path to configuration file", required=False)
    args = parser.parse_args()
    if args.create_daemon:
        create_daemon()
    elif args.create_config:
        create_config(args.config_file)
    elif args.config_file:
        run(args.config_file)
    else:
        parser.error('need arguments')


if __name__ == '__main__':
    main()

exit(0)
