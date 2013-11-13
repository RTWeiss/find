import sys,pymysql,re

def delete(row):
    sql.execute("DELETE FROM links WHERE id=" + row[0])

def update(row, field, value):
    sql.execute("UPDATE links SET $s=$s WHERE id=$s" %(field, value, row[0]))

def select(field='id', value='*'):
    sql.execute("SELECT * FROM links WHERE %s=%s" %(field, value))
    return sql.fetchall()



sql = pymysql.connect(user='testpy', db='crawler').cursor()
#sql.execute("INSERT INTO links(url, parsed) VALUES('http://google.com', 1)")
rows = select('parsed', 1)
for row in rows:
    print(row)


if len(sys.argv)>1:
    start = sys.argv[1]

