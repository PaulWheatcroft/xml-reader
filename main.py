import os
import psycopg

os.environ['PGHOST'] = 'generally-busy-robin-iad.a1.pgedge.io'
os.environ['PGUSER'] = 'admin'
os.environ['PGDATABASE'] = 'perlego_interview'
os.environ['PGSSLMODE'] = 'require'
os.environ['PGPASSWORD'] = '1AZwRsAH049P4132WG8Vmt2P'


def main():
    connection = psycopg.connect()
    cursor = connection.cursor()
    cursor.execute('SELECT node_name FROM spock.node')
    node_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    print(node_names)


if __name__ == '__main__':
    main()
