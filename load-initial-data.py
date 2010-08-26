from pysqlite2 import dbapi2 as S
import socket, struct, psyco, time

in_memory=False
with_index=True

#print socket.inet_ntoa(struct.pack('>L', int("35651584")))

def load():
    if in_memory:
        dbid = ":memory:"
    else:
        dbid = "geoip.db"

    print dbid
    c = S.connect(dbid)

    try:
        c.execute("drop table a")
    except:
        pass

    c.execute("create table a (a1 integer, a2 integer, c1 varchar2(2), c2 varchar2(3), c3 varchar2(255))")

    c.execute("begin")

    for line in open("geoip-raw.txt").xreadlines():
        if line[0] == '#': continue
        d = line.split("\"")
        c.execute("""insert into a values (%s, %s, "%s", "%s", "%s")""" % (d[1], d[3], d[9].lower(), d[11].lower(), d[13].lower()))

    for r in c.execute("select count(*) from a"): print r[0]

    c.commit()

    if with_index:
        # fast index
        c.execute("create index a_a1_a2 on a(a1, a2, c1, c2, c3)")

    c.close()

def query():
    c = S.connect("geoip.db")

    addr = "1.2.3.4"
    a = struct.unpack('<L', socket.inet_aton(addr))[0]

    start = time.time()

    for x in range(100000):
        for r in c.execute("select * from a where a1 <= %d and a2 >= %d" % (a, a)):
            j = r

    print '%.3f seconds' % (time.time() - start)

    c.close()

#load()
print "Q"
query()

# ---
