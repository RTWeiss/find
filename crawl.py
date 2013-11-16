
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

def select(field='id', value='', newUrl=False, skippin=False):
    if newUrl:
        sql.execute("SELECT * FROM links WHERE %s='%s' and LENGTH(linkedto) > 10" %(field, value))
    elif skippin:
        sql.execute("SELECT * FROM links WHERE %s='%s' and MOD(id, 4)=%s" %(field, value, skippin))
    elif value != '':
        sql.execute("SELECT * FROM links WHERE %s='%s'" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    resp = sql.fetchall()
    if resp:
        return resp[0]
    else:
        return ()

def insert(url, linkedto='0', title='', description='', h1=''):
    sql.execute("INSERT INTO links(url, parsed, linkedto, title, descr) VALUES('%s', 0, '%s', '%s', '%s')" %(url, linkedto, title, description))


def email(address, site):
    sql.execute("SELECT * FROM emails WHERE address='%s'" %address)
    if sql.fetchall() == ():
        sql.execute("INSERT INTO emails(address, site) VALUES('%s', '%s')" %(address, site))

def dbdomain(domain):
    sql.execute("SELECT * FROM domains WHERE domain='%s'" %domain)
    x = sql.fetchall()
    if x == ():
        sql.execute("INSERT INTO domains(domain) VALUES('%s')" %(domain))
        return True
    return False

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

def domain(url):
    subs = url[7:url.find('/', 8)]
    subs = subs.split('.')
    ret = subs[0]
    for x in range(len(subs)):
        if len(subs[-x]) > 3:
            ret = subs[-x]
    while subs[0] != ret:
        subs.pop(0)
    return subs[0], 'http://'+'.'.join(subs) + url[url.find('/', 8):]

def reset():
    sql.execute("DROP TABLE IF EXISTS links")
    sql.execute("DROP TABLE IF EXISTS domains")
    #sql.execute("DROP TABLE IF EXISTS emails")
    sql.execute("DROP TABLE IF EXISTS keywords")
    sql.execute("CREATE TABLE links(id INT PRIMARY KEY AUTO_INCREMENT, url VARCHAR(256), parsed TINYINT(1), linkedto TEXT, title VARCHAR(128), descr VARCHAR(256), h1 VARCHAR(256))")
    #sql.execute("CREATE TABLE emails(id INT PRIMARY KEY AUTO_INCREMENT, address VARCHAR(256), site VARCHAR(256))")
    sql.execute("CREATE TABLE domains(id INT PRIMARY KEY AUTO_INCREMENT, domain VARCHAR(256))")
    sql.execute("CREATE TABLE keywords(word VARCHAR(40), ids TEXT)")

 # Connection to the server

mysql = pymysql.connect(user='testpy', db='crawler', charset='utf8')
sql = mysql.cursor()
 # The initial URL to parse. Either a user-defined one or the first one in the table.
start = 0
manual=False
if len(sys.argv)>1:
    skip = sys.argv[1]
    if skip not in ['1','2','3','4','5','6','7','8','9']:
        skipping=False
        start=skip
        skip = False
    else:
        skip = int(skip)
    manual=True
    idstart = getId(start)
    if not idstart:
        insert(start)

# -----END MYSQL BLOCK-----






# -----BEGIN PARSER BLOCK-----

def parse(url):

    # I request the HTML code.
    try:
        html=urlopen(url, timeout=5).read().decode('ISO-8859-1')
    except:
        return 'crash',0,0,0,0

     # I look for links, titles, meta-data and headings.

    links = re.findall( r"""<a\s+.*?href=['"](.*?)['"].*?(?:</a|/)>""", html)
    links += re.findall( r"""<link\s+.*?href=['"](.*?)['"].*?(?:</link|/|)>""", html)
    title = (re.findall( r'<title>(.*?)</title>', html) + [''])[0]
    keywords = (re.findall( r"""<meta name="keywords" content=['"](.*?)['"]>""", html)+[''])[0]
    if title.count('>'):
        title=title[:title.find('>')]
    description = (re.findall( r"""<meta name="description" content=['"](.*?)['"]\s+.*?>""", html)+[''])[0]
    if description.count('>'):
        description=description[:description.find('>')]
    emails = (re.findall( r"""\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b""", html))
    for em in emails:
        print(em)
        email(url, em)

    dom = domain(url)[0]
    if not title:
        title = dom
    # Gets really messy from here (if it wasn't already messy enough for you).
    i,h1 = 1, []
    while not len(h1) and i < 7:
        h1 = re.findall( r'<h%s>(.*?)</h%s>' %(i, i), html)
        i += 1
    h1 = (h1 + [''])[0]
    while h1.count('<'):
        spot = h1.find('<')
        h1 = h1[:spot]+h1[h1.find('>', spot)+1:]
    if not description:
        description = dom[0].upper() + dom[1:] + ' - ' + h1
    ret = [links]
    for ttl in [title, keywords, description, h1]:
        ttl = ''.join(c for c in ttl if c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;?@[\\]^_`{|}~– \t\n\r')
        ret.append(ttl)
    return ret

# -----END PARSER BLOCK




# -----BEGIN CRAWLER BLOCK-----

def checkUrl(url, link):
    if url[:11]=='javascript:' or '>' in url or '<' in url or '.' not in url or '{' in url or '}' in url:
        return ''
    if url.find('?') != -1:
        url = url[:url.find('?')]
    if url.find(':', 7) != -1:
        url = url[:url.find(':', 7)]
    if url[:7]=='mailto:':
        url = url[7:]
        email(url, link)
        return url
    url = url.replace('https://', 'http://')
    if url[:1]=='/':
        url = link+url
    if url[:4] != 'http':
        url = 'http://'+url
    if url[-1] != '/':
        url += '/'
    #if url[-5:] == '.png/' or url[-5:] == '.jpg/' or url[-5:] == '.gif/':
     #   return ''
    ht = url.find('//') + 2
    for w in ['www.', 'www2.', 'www1.']:
        if url[ht:ht+4]==w:
            url = url[:ht]+url[ht+len(w):]
    if url[:url.find('/', ht)].count('.') > 1:
        end1 = url.find('.') + 1
        second = url[end1:url.find('.', end1)]
        if len(second) > 3 and second != 'tumblr':
            url = url[:ht] + url[end1:]
    url = domain(url)[1]
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
        linkId = getId(link)
        print(linkId % 4)
        print(link)
        if not dbdomain(domain(link)[0]) and not manual:
            update(linkId, 'parsed', '1')
            if skip:
                start = select('parsed', '0', skippin=skip)[1]
            else:
                start = select('parsed', '0', True)[1]
            continue
        manual = False
        mysql.commit()
        [linksl, title, keywords, description,h1] = parse(link)
        if linksl=='crash':
            print('404')
            delete(link)
            if skip:
                start = select('parsed', '0', skippin=skip)[1]
            else:
                start = select('parsed', '0', True)[1]
            continue

        string = ""
        for x in [title + ' ' + title + ' ' + keywords + ' ' + description + ' ' + h1]:
            string += ''.join([e for e in x.lower() if e.isalnum() or e==' '])
        string = [x for x in string.split(' ') if x not in ['', ' ', 'the', 'of', 'or']]
        for x in range(4):
            string += [domain(link)[0]]
        if linksl:
            links = []
            for l in linksl:
                l = baseUrl(checkUrl(l, link))
                if l not in links:
                    links.append(l)
            for linkn in links:
                if linkn=='':
                    continue
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
        #update(linkId, 'parsed', '1')
        update(linkId, 'title', str(title.replace("'",  '`')))
        update(linkId, 'descr', str(description.replace("'", '`')))
        update(linkId, 'h1', str(h1.replace("'", '`')))
        if skip:
            start = select('parsed', '0',skippin=skip)[1]
        else:
            start = select('parsed', '0', True)[1]
        update(getId(start), 'parsed', '1')
        #mysql.commit()
except KeyboardInterrupt:
    print('Saving...')
    update(linkId, 'parsed', '0')

# -----END CRAWLER BLOCK-----







# -----BEGIN FOOTER BLOCK-----

mysql.commit()
sql.close()

# -----END FOOTER BLOCK-----

