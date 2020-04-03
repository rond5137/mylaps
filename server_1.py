import asyncio
import logging
import concurrent.futures
from messages import Message
from db_connector import DBConnector


class Server:
    def __init__(self, host, port, server_name,
                 db_name, db_user, db_password, db_host,
                 loop=None):
        self.server_name = server_name
        self.db = DBConnector(
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
            db_host=db_host
        )
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
        logging.info(f'Accepted connection from {peername}')
        while not reader.at_eof():
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=3600.0)
                if not data:
                    break
                msg = Message(self.server_name)
                parsed_response = msg.get(data)
                if parsed_response['count'] > 0:
                    self.db.insert(
                        parsed_response['type'],
                        parsed_response['location'],
                        parsed_response['data']
                    )
                if resp:=msg.response:
                    writer.write(resp)
            except (concurrent.futures.TimeoutError, asyncio.TimeoutError):
                continue
        writer.close()
        logging.info(f'Closed connection from {peername}')


if __name__ == '__main__':
    try:
        import settings
    except ModuleNotFoundError:
        logging.error('No settings.py file!')
        exit(1)
    logging.basicConfig(level=logging.DEBUG)
    server = Server(
        host=settings.host,
        port=settings.port,
        server_name=settings.server_name,
        db_name=settings.db_name,
        db_user=settings.db_user,
        db_password=settings.db_password,
        db_host=settings.db_host
    )
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
