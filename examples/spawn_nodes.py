import logging
import asyncio
from typing import Literal

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log = logging.getLogger("kademlia")
log.addHandler(handler)
log.setLevel(logging.DEBUG)


BOOTSTRAP_PORT = 8468


async def start_bootstrap_node(port) -> Server:
    server = Server()
    await server.listen(port)
    log.info(f"Port {port}: Started bootstrap".format(port))
    return server


async def start_node(port: int, bootstrap_port: int) -> Server:
    server = Server()
    await server.listen(port)
    bootstrap_node = ("localhost", bootstrap_port)
    await server.bootstrap([bootstrap_node])
    log.info(f"Port {port}: Started node")
    return server


async def main():
    asyncio.ensure_future(start_bootstrap_node(BOOTSTRAP_PORT))

    for port in range(9000, 9031):
        asyncio.ensure_future(start_node(port, BOOTSTRAP_PORT))

    await asyncio.gather(*asyncio.all_tasks())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
