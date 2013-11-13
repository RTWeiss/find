
# -----BEGIN HEADER BLOCK-----

 # File:             crawler.crawl.py

 # Description:      The main body of the program.

 # Requirements:     pymysql, python3

 # Author:           Noah Ingham

# -----END HEADER BLOCK-----


import sys,pymysql,re
from urllib.request import urlopen


# -----BEGIN MYSQL BLOCK-----

parsed='parsed'
id='id'


 # Defining python functions for common SQL calls

def delete(row):
    sql.execute("DELETE FROM links WHERE id=" + row[0])

def update(row, field, value):
    sql.execute("UPDATE links SET $s=$s WHERE id=$s" %(field, value, row[0]))

def select(field=id, value=False):
    if value:
        sql.execute("SELECT * FROM links WHERE %s=%s" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    return sql.fetchall()

def insert(url):
    sql.execute("INSERT INTO links(url, parsed) VALUES('%s', 0)" %(url))

def email(address, site):
    sql.execute("INSERT INTO emails(adrress, site) VALUES(%s, %s)" %(address, site))

 # Connection to the server

mysql = pymysql.connect(user='testpy', db='crawler')
sql = mysql.cursor()


 # The initial URL to parse. Either a user-defined one or the first one in the table.

if len(sys.argv)>1:
    start = sys.argv[1]
else:
    rows = select(parsed, 0)
    start = select(parsed, 0)[0][1]

# -----END MYSQL BLOCK-----






# -----BEGIN PARSER BLOCK-----

def parse(url):

     # I request the HTML code.

    html=urlopen(url).read().decode('utf-8')

     # I look for links, titles, meta-data and headings.

    links = re.findall( r"""<a\s+.*?href=['"](.*?)['"].*?(?:</a|/)>""", html)
    title = re.findall( r'<title>(.*?)</title>', html)
    keywords = re.findall( r"""<meta name="keywords" content=['"](.*?)['"]>""", html)
    description = re.findall( r"""<meta name="description" content=['"](.*?)['"]>""", html)
    h1 = re.findall( r'<h1>(.*?)</h1>', html)
    words = [x.lower().strip("""#"'/?.@""") for x in title + keywords + description + h1]
    words = list(set(words))
    print(words)
    print(links)

parse(start)

# -----END PARSER BLOCK






# -----BEGIN FOOTER BLOCK

mysql.commit()
sql.close()

# -----END FOOTER BLOCK
