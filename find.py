
# -----BEGIN HEADER BLOCK-----

 # File:             crawler.find.py

 # Description:      The search engine interface.

 # Requirements:     Pymysql, Python3, Access to a mysql server

 # Author:           Noah Ingham

# -----END HEADER BLOCK-----


import sys,pymysql,math

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
    sql.execute("SELECT * FROM keywords WHERE word LIKE '%" + string + "%'")# ORDER BY LENGTH(ids) DESC")
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


# -----END MYSQL BLOCK-----


# -----START LOOKUP BLOCK-----

def look(lookup):
    global sql

    dicti = {}
    resplist=[]
    respi = ''
    #for x in lookup.split(' '):
    #    xlookup = lookUp(x)[0]
    #    resplist.append(xlookup)
    #    respi += xlookup[1]
    respi=lookUp(lookup)
    if not respi:
        print('No results. Multiple words at a time are not yet supported.')
        return False, False
    else:
        for resp in respi:
            idl = resp[1].split(', ')
            for n in idl:
                whole = select('id', n)
                if whole:
                    if whole in dicti:
                        dicti[whole] *= 1.3
                    else:
                        ret = 0
                        for ids in whole[3].split(', '):
                            idscore = select('id', ids)
                            if idscore:
                                idscore = len(idscore[3])
                            else:
                                idscore = 1
                            idscore = (math.log(idscore, 10))
                            if ids in idl:
                                ret += 2+idscore
                            else:
                                ret += 0.5+idscore
                        dicti[whole] = round(ret)
                        #dicti[whole] = whole[3].count(',')

        ordl = sorted(dicti.items(), key=lambda x: x[1], reverse=True)
        return ordl, dicti
# -----END LOOKUP BLOCK-----



# -----BEGIN FOOTER BLOCK-----
if __name__=='__main__':
    if len(sys.argv)>1:
        lookup=''
        #for x in range(len(sys.argv)-1):
        lookup = sys.argv[1]
    else:
        lookup = input('>>> ')
    ordl = look(lookup)

    for result in ordl:
        result = result[0]
        print('')
        if result[4] != ' ':
            print(result[4])
        if result[5] != ' ':
            print(result[5])
        print('\033[95m'+result[1]+'\033[0m')
    sql.close()

# -----END FOOTER BLOCK-----

