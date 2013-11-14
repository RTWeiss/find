
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
    sql.execute("UPDATE links SET %s='%s' WHERE id='%s'" %(field, value, row))

def select(field=id, value=False):
    if value:
        sql.execute("SELECT * FROM links WHERE %s='%s'" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    resp = sql.fetchall()
    if resp:
        return resp[0]
    else:
        return ()

def insert(url, linkedto=[], title='', description=''):
    sql.execute("INSERT INTO links(url, parsed, linkedto, title, descr) VALUES('%s', 0, '%s', '%s', '%s')" %(url, linkedto, title, description))


def email(address, site):
    sql.execute("INSERT INTO emails(address, site) VALUES('%s', '%s')" %(address, site))

def keyword(word, url):
    urlId = select('url', url)
    sql.execute("INSERT INTO keywords(words, ids) VALUES('%s', '%s')" %(word, urlId))

def incrementor():
    sql.execute("SHOW TABLE STATUS LIKE 'links'")
    return sql.fetchall()[0][10]

def getId(url):
    sel = select('url', url)
    return sel[0]


def reset():
    sql.execute("DROP TABLE IF EXISTS links")
    sql.execute("DROP TABLE IF EXISTS emails")
    sql.execute("DROP TABLE IF EXISTS keywords")
    sql.execute("CREATE TABLE links(id INT PRIMARY KEY AUTO_INCREMENT, url VARCHAR(256), parsed TINYINT(1), linkedto TEXT, title VARCHAR(128), descr VARCHAR(256))")
    sql.execute("CREATE TABLE emails(id INT PRIMARY KEY AUTO_INCREMENT, address VARCHAR(256), site VARCHAR(256))")
    sql.execute("CREATE TABLE keywords(word VARCHAR(40), ids TEXT)")

 # Connection to the server

mysql = pymysql.connect(user='testpy', db='crawler')
sql = mysql.cursor()
reset()
insert('http://google.com/', '0')

 # The initial URL to parse. Either a user-defined one or the first one in the table.

if len(sys.argv)>1:
    start = sys.argv[1]
else:
    start = select(parsed, 0)[1]

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
    if url[8:12]=='www.':
        url = url[:8]+url[12:]
    return url

def baseUrl(url):
    if url[:4]=='http':
        return url[:url.find('/',8)+1]
    else:
        return checkUrl(url[url.find('@')+1:], '')


link = start
start = select(parsed, 0)[1]
linkId = getId(link)
linksl, title, keywords, description,h1 = parse(link)
for check in [title, keywords, description, h1]:
    if not check:
        check += ' '
string = ""
for x in (title + keywords + description + h1):
    string += ''.join([e for e in x.lower() if e.isalnum() or e==' '])
string = [x for x in set(string.split(' ')) if x != '']

links = []
for l in linksl:
    l = baseUrl(checkUrl(l, link))
    if l not in links:
        links.append(l)
for linkn in links:
    li = select('url', linkn)
    print('\t%s' %linkn)
    if len(li) == 0:
        insert(linkn, linkId)
    else:
        idh = li[0]
        linkedto = li[3]
        if link not in linkedto:
            linkedto += ', ' + str(linkId)
        update(idh, 'linkedto', linkedto)
for key in string:
    print(key)
    #li = select('word', 'google')

# -----END CRAWLER BLOCK-----







# -----BEGIN FOOTER BLOCK

mysql.commit()
sql.close()

# -----END FOOTER BLOCK

