
# -----BEGIN HEADER BLOCK-----

 # File:             crawler.crawl.py

 # Description:      The main body of the program.

 # Requirements:     Pymysql, Python3, Access to a mysql server

 # Author:           Noah Ingham

# -----END HEADER BLOCK-----


import sys,pymysql,re
from urllib.request import urlopen


# -----BEGIN MYSQL BLOCK-----



 # Defining python functions for common SQL calls

def delete(url):
    id = select('url', url)[0]
    if id:
        sql.execute("DELETE FROM links WHERE id=%s" %(id))

def update(row, field, value):
        sql.execute("UPDATE links SET %s='%s' WHERE id='%s'" %(field, value, row))

def select(field='id', value=''):
    if value != '':
        sql.execute("SELECT * FROM links WHERE %s='%s'" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    resp = sql.fetchall()
    if resp:
        return resp[0]
    else:
        return ()

def insert(url, linkedto='0', title='', description=''):
    sql.execute("INSERT INTO links(url, parsed, linkedto, title, descr) VALUES('%s', 0, '%s', '%s', '%s')" %(url, linkedto, title, description))


def email(address, site):
    sql.execute("INSERT INTO emails(address, site) VALUES('%s', '%s')" %(address, site))

def keyword(word, url):
    sql.execute("SELECT * FROM keywords WHERE word='%s'" %(word))
    resp = sql.fetchall()
    if  len(resp) > 0:
        ids = resp[0][1]
        sql.execute("UPDATE keywords SET ids='%s' WHERE word='%s'" %(ids + ', ' + str(url), word))
    else:
        sql.execute("INSERT INTO keywords(word, ids) VALUES('%s', '%s')" %(word, url))

def incrementor():
    sql.execute("SHOW TABLE STATUS LIKE 'links'")
    return sql.fetchall()[0][10]

def getId(url):
    sel = select('url', url)
    if len(sel) == 0:
        return 0
    return sel[0]


def reset():
    sql.execute("DROP TABLE IF EXISTS links")
    sql.execute("DROP TABLE IF EXISTS emails")
    sql.execute("DROP TABLE IF EXISTS keywords")
    sql.execute("CREATE TABLE links(id INT PRIMARY KEY AUTO_INCREMENT, url VARCHAR(256), parsed TINYINT(1), linkedto TEXT, title VARCHAR(128), descr VARCHAR(256))")
    sql.execute("CREATE TABLE emails(id INT PRIMARY KEY AUTO_INCREMENT, address VARCHAR(256), site VARCHAR(256))")
    sql.execute("CREATE TABLE keywords(word VARCHAR(40), ids TEXT)")

 # Connection to the server

mysql = pymysql.connect(user='testpy', db='crawler', charset='utf8')
sql = mysql.cursor()
#insert('http://google.com/', '0')
 # The initial URL to parse. Either a user-defined one or the first one in the table.
start = 0
if len(sys.argv)>1:
    start = sys.argv[1]
    idstart = getId(start)
    if not idstart:
        insert(start)
if len(sys.argv)>2:
    reset()
# -----END MYSQL BLOCK-----






# -----BEGIN PARSER BLOCK-----

def parse(url):

    # I request the HTML code.
    try:
        html=urlopen(url).read().decode('utf8')
    except:
        return 'crash',0,0,0,0
    #for code in ['\u2022','\u0153', '\u2021', '\u0178', '\u201e', '\u2014', '\u2013', '\u2019']:
    #    html = html.replace(code, '')

     # I look for links, titles, meta-data and headings.

    links = re.findall( r"""<a\s+.*?href=['"](.*?)['"].*?(?:</a|/)>""", html)
    links += re.findall( r"""<link\s+.*?href=['"](.*?)['"].*?(?:</link|/|)>""", html)
    title = re.findall( r'<title>(.*?)</title>', html)
    keywords = re.findall( r"""<meta name="keywords" content=['"](.*?)['"]>""", html)
    description = re.findall( r"""<meta name="description" content=['"](.*?)['"/]>""", html)
    h1 = re.findall( r'<h1>(.*?)</h1>', html)
    return links, title, keywords, description, h1

# -----END PARSER BLOCK




# -----BEGIN CRAWLER BLOCK-----

def checkUrl(url, link):
    if url.find('?') != -1:
        url = url[:url.find('?')]
    if url[:7]=='mailto:':
        url = url[7:]
        email(url, link)
        return url
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
    if url[7:12]=='www1.':
        url = url[:7]+url[12:]
    if url[8:13]=='www1.':
        url = url[:8]+url[13:]
    if url[7:12]=='www2.':
        url = url[:7]+url[12:]
    if url[8:13]=='www2.':
        url = url[:8]+url[13:]
    return url

def baseUrl(url):
    if url[:4]=='http':
        return url[:url.find('/',8)+1]
    else:
        return checkUrl(url[url.find('@')+1:], '')

if not start:
    start = select('parsed', '0')[1]
try:
    while True:
        link = start
        print(link)
        linkId = getId(link)
        linksl, title, keywords, description,h1 = parse(link)
        if linksl=='crash':
            delete(link)
            start = select('parsed', '0')[1]
            continue

        for check in [title, keywords, description, h1]:
            if not check:
                check.append(' ')
        string = ""
        for x in (title + keywords + description + h1):
            string += ''.join([e for e in x.lower() if e.isalnum() or e==' '])
        string = [x for x in set(string.split(' ')) if x != '']
        if linksl:
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
                    if str(linkId) not in linkedto:
                        linkedto += ', ' + str(linkId)
                    update(idh, 'linkedto', linkedto)
        for key in string:
            keyword(key, linkId)
        update(linkId, 'parsed', '1')
        update(linkId, 'title', str(title[0].replace("'", '"')))
        update(linkId, 'descr', str(description[0].replace("'", '`')))
        start = select('parsed', '0')[1]
        mysql.commit()
except KeyboardInterrupt:
    print('Saving...')

# -----END CRAWLER BLOCK-----







# -----BEGIN FOOTER BLOCK

mysql.commit()
sql.close()

# -----END FOOTER BLOCK

