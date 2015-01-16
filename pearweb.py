#!/usr/bin/env python3
# vim:fileencoding=utf-8:ts=8:et:sw=4:sts=4:tw=79

"""
pearweb.py

The (exceedingly simple) web page for the PearBot IRC bot.

Copyright (c) 2015 Twisted Pear <pear at twistedpear dot at>
See the file LICENSE for copying permission.
"""

import asyncio
import logging
import signal
from aiohttp import web
from os import getenv

LOG_FORMAT = "{asctime} [{process}] {levelname}({name}): {message}"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, style="{")


@asyncio.coroutine
def handle_root(request):
    return web.Response(text="Hello, World!")

if __name__ == "__main__":
    logger = logging.getLogger("pearweb")
    logger.info("Starting pearweb asyncio webserver...")

    logger.info("Setting up application routes...")
    app = web.Application()
    app.router.add_route("GET", "/", handle_root)

    port = int(getenv("PORT", 5000))
    logger.info("Creating server on port {port}...".format(port=port))
    loop = asyncio.get_event_loop()
    coro = loop.create_server(app.make_handler(), port=port)

    serv = loop.run_until_complete(coro)

    def shutdown():
        logger.info("Shutting down webserver...")
        serv.close()

    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)

    loop.run_until_complete(serv.wait_closed())
    logger.info("Exiting...")