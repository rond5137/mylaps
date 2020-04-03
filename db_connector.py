import psycopg2
import logging


class DBConnector:
    def __init__(self, db_name, db_user, db_password, db_host):
        self.user = db_user
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host
            )
            self.cursor = self.conn.cursor()
            self._create_tables()
        except psycopg2.OperationalError as err:
            logging.error(err)

    def __del__(self):
        self.conn.close()

    def insert(self, message_type: str, location: str, messages: list):
        if message_type == 'Marker':
            table = 'markers'
        elif message_type == 'Passing':
            table = 'passings'
        else:
            return None
        for message in messages:
            self.cursor.execute(f'''
            insert into {table} (location,{",".join(message.keys())})
            values ('{location}',{",".join([str(f"'{m}'") for m in message.values()])})
            ''')
        self.conn.commit()

    def _create_tables(self):
        self.cursor.execute(f'''
        create table IF NOT EXISTS passings
        (
            id serial not null constraint passings_pk primary key,
            location    char(1024),
            c           char(7),
            ct          char(2),
            t           char(512),
            ts          char(512),
            d           char(512),
            l           char(512),
            dv          char(512),
            re          char(512),
            an          char(8),
            am          char(512),
            ans         char(512),
            ana         char(512),
            dm          char(512),
            g           char(512),
            h           char(512),
            n           char(1024),
            b           char(512),
            bid         char(512)
        );
        
        alter table passings owner to {self.user};
        create unique index IF NOT EXISTS passings_id_uindex on passings (id);
        ''')

        self.cursor.execute(f'''
        create table IF NOT EXISTS markers
        (
            id serial not null constraint markers_pk primary key,
            location    char(1024),
            mt          char(1024),
            t           char(512),
            n           char(1024)
        );
        
        alter table markers owner to {self.user};
        create unique index IF NOT EXISTS markers_id_uindex on markers (id);
        ''')
        self.conn.commit()

    def _create_db(self):
        pass
        # CREATE DATABASE mylaps_test
        #   WITH OWNER = postgres
        #        ENCODING = 'UTF8'
        #        TABLESPACE = pg_default
        #        LC_COLLATE = 'ru_RU.UTF-8'
        #        LC_CTYPE = 'ru_RU.UTF-8'
        #        CONNECTION LIMIT = -1;
