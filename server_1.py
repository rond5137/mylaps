import asyncio
import logging
import concurrent.futures
from messages import Message
from db_connector import DBConnector


class EchoServer:
    server_name = 'RondServer'
    db = DBConnector()

    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)

    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        logging.info('Listening established on {0}'.format(self._server.sockets[0].getsockname()))
        if and_loop:
            self._loop.run_forever()

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    async def handle_connection(self, reader, writer):
        peername = writer.get_extra_info('peername')
        logging.info('Accepted connection from {}'.format(peername))
        while not reader.at_eof():
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=10.0)
                print(f'<<< {data}')
                if not data:
                    break
                msg = Message(self.server_name)
                parsed_response = msg.get(data)
                if resp:=msg.response:
                    print(f'>>> {resp}')
                    writer.write(resp)
            except (concurrent.futures.TimeoutError, asyncio.exceptions.TimeoutError):
                continue
        writer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = EchoServer('', 3097)
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()