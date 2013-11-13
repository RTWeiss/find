
# -----BEGIN HEADER BLOCK-----

 # File:             crawler.crawl.py

 # Description:      The main body of the program.

 # Requirements:     Pymysql, Python3, Access to a mysql server

 # Author:           Noah Ingham

# -----END HEADER BLOCK-----


import sys,pymysql,re
from urllib.request import urlopen


# -----BEGIN MYSQL BLOCK-----

parsed='parsed'
id='id'


 # Defining python functions for common SQL calls

def delete(row):
    sql.execute("DELETE FROM links WHERE id=%s" %(row[0]))

def update(row, field, value):
    sql.execute("UPDATE links SET %s=%s WHERE id=%s" %(field, value, row[0]))

def select(field=id, value=False):
    if value:
        sql.execute("SELECT * FROM links WHERE %s='%s'" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    return sql.fetchall()

def insert(url):
    sql.execute("INSERT INTO links(url, parsed) VALUES('%s', 0)" %(url))

def email(address, site):
    sql.execute("INSERT INTO emails(address, site) VALUES('%s', '%s')" %(address, site))

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
    return links, title, keywords, description, h1

# -----END PARSER BLOCK











# -----BEGIN CRAWLER BLOCK-----

def checkUrl(url, link):
    if url[:7]=='mailto:':
        email(url, link)
        return url[7:]
    elif url[:7]!='http://' and url[:8]!='https://':
        url = link+url
    if url[:4] != 'http':
        url = 'http://'+url
    if url[-1] != '/':
        url += '/'
    if url[7:11]=='www.':
        url = url[:7]+url[11:]
    if url[8:11]=='www.':
        url = url[:8]+url[12:]
    return url

def baseUrl(url):
    if url[:4]=='http':
        return url[:url.find('/',8)+1]
    else:
        return checkUrl(url[url.find('@')+1:], '')
link = start
linksl, title, keywords, description,h1 = parse(link)

string = ""
for x in (title + keywords + description + h1):
    string += ''.join([e for e in x.lower() if e.isalnum() or e==' '])
string = list(set(string.split(' ')))

links = []
for l in linksl:
    if l not in links:
        links.append(l)
for url in links:
    url=checkUrl(url, link)
    print(baseUrl(url))

# -----END CRAWLER BLOCK-----









# -----BEGIN FOOTER BLOCK

mysql.commit()
sql.close()

# -----END FOOTER BLOCK

