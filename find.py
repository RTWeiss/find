
# -----BEGIN HEADER BLOCK-----

 # File:             crawler.crawl.py

 # Description:      The main body of the program.

 # Requirements:     Pymysql, Python3, Access to a mysql server

 # Author:           Noah Ingham

# -----END HEADER BLOCK-----


import sys,pymysql,re

# -----BEGIN MYSQL BLOCK-----


 # Defining python functions for common SQL calls

def select(field=id, value=''):
    if value != '':
        sql.execute("SELECT * FROM links WHERE %s='%s'" %(field, value))
    else:
        sql.execute("SELECT * FROM links")
    resp = sql.fetchall()
    if resp:
        return resp[0]
    else:
        return ()

def lookUp(string):
    sql.execute("SELECT * FROM keywords WHERE word LIKE '%" + string + "%' ORDER BY LENGTH(ids) DESC")
    resp = sql.fetchall()
    return resp

def email(address):
    sql.execute("SELECT * FROM emails WHERE address='%s'" %(addres))

def getUrl(id):
    sel = select('id', id)
    if len(sel) == 0:
        return 0
    return sel[0]

 # Connection to the server

mysql = pymysql.connect(user='testpy', db='crawler')
sql = mysql.cursor()

if len(sys.argv)>1:
    lookup = sys.argv[1]
else:
    lookup = input('>>> ')

# -----END MYSQL BLOCK-----


# -----START LOOKUP BLOCK-----
dicti = {}
resp = lookUp(lookup)
if not resp:
    print('No results.')
else:
    for n in resp[0][1].split(', '):
        whole = select('id', n)
        if n != '0':
            dicti[whole] = whole[3].count(',')

    ordl = sorted(dicti.items(), key=lambda x: x[1], reverse=True)

    for result in ordl[:6]:
        result = result[0]
        print('')
        if result[4] != ' ':
            print(result[4])
        if result[5] != ' ':
            print(result[5])
        print('\033[95m'+result[1]+'\033[0m')

# -----END LOOKUP BLOCK






# -----BEGIN FOOTER BLOCK

sql.close()

# -----END FOOTER BLOCK

