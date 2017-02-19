import psycopg2

URI = 'postgres://admin:WUGBALEUAAZORBDF@sl-us-dal-9-portal.4.dblayer.com:19955/compose'

conn = psycopg2.connect(URI)

cur = conn.cursor()

people = ['clinton', 'bush', 'homer', 'jackson', 'kanye', 'kennedy', 'lincoln',
          'obama', 'reagan', 'roosevelt', 'stalin', 'trump', 'washington']

for person in people:
    with open('out/{}.txt'.format(person), 'r') as f:
        i = 0
        for line in f:
            cur.execute('insert into generated (person, output_id, output) values (%s, %s, %s)',
                        (person, i, line.strip('\n')))
            i += 1
            if (i % 50) == 0:
                conn.commit()
conn.commit()