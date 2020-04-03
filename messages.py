import logging


class Message:
    def __init__(self, server_name: str = None):
        self.protocol = 'Version2.1'
        self.server_name = server_name or 'DefaultServer'
        self.message: str = ''
        self.message_type: str = ''
        self.message_number: str = ''
        self.message_data: list = []
        self.location: str = ''
        self.responses = {
            'Pong': f'{self.server_name}@AckPong@{self.protocol}@$',
            'Marker': '{}@AckPassing@{}@$',
            'Passing': '{}@AckPassing@{}@$',
        }

    def get(self, data: bytes):
        self.message = data.decode('utf-8')
        self._parse_message()
        return_data = {
            'type': self.message_type,
            'location': self.location,
            'count': len(self.message_data),
            'data': self.message_data
        }
        return return_data

    def _parse_message(self):
        try:
            splitted_msg: list = self.message.split('@')
            self.location = splitted_msg[0]
            self.message_type = splitted_msg[1]
            self.message_number = splitted_msg[-2]
            raw_message_data = list(splitted_msg[2:-2])
            for i in raw_message_data:
                d = {}
                for ii in i.split('|'):
                    k, v = ii.split('=')
                    d[k] = v
                self.message_data.append(d)
        except Exception as e:
            logging.error(f'Message parsing error - {e}')

    @property
    def response(self) -> bytes or None:
        resp = self.responses.get(self.message_type, '').format(self.server_name, self.message_number)
        if resp:
            return resp.encode()
        else:
            return None
