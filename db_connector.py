import psycopg2


class DBConnector:
    dbname = 'mylaps_test'
    user = 'rond'
    password = '5137'
    host = 'localhost'

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cursor = self.conn.cursor()
            self._create_tables()
        except psycopg2.OperationalError as err:
            print(err)


    def __del__(self):
        self.conn.close()
        print('connection closed')

    def insert(self, messages: list):

        for m in messages:
            pass

    def _create_tables(self):

        self.cursor.execute(f'''
        create table IF NOT EXISTS passings
        (
            id serial  not null
                constraint passings_pk
                    primary key,
            c  char(7) not null,
            ct char(2) not null,
            t  time    not null,
            d  date    not null,
            l  integer not null,
            dv integer not null,
            re integer not null,
            an char(8) not null,
            g  integer not null,
            n  char(1024)
        );
        
        alter table passings
            owner to {self.user};
        
        create unique index IF NOT EXISTS passings_id_uindex
            on passings (id);
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
