
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


# -----END MYSQL BLOCK-----


# -----START LOOKUP BLOCK-----

def look(lookup):
    global sql
    lookup = lookup[0]
    dicti = {}
    resplist=[]
    respi = ''
    #for x in lookup.split(' '):
    #    xlookup = lookUp(x)[0]
    #    resplist.append(xlookup)
    #    respi += xlookup[1[

    respi=[x for y in lookUp(lookup) for x in y[1].split(', ')] # Create a list of ids from each keyword
    respi = [(a, respi.count(a)) for a in set(respi)] # Count each one
    respi = sorted(respi, key=lambda x: x[1], reverse=True) # Sort them

    if not respi:
        print('No results. Multiple words at a time are not yet supported.')
        return False, False
    else:
        for n in respi[:round(len(respi))]:
            whole = select('id', n[0])
            if whole:
                ret = 2
                for ids in whole[3].split(', '):
                    idscore = select('id', ids)
                    if idscore:
                        idscore = len(idscore[3])
                    else:
                        idscore = 1
                    idscore = (math.log(idscore, 10))
                    if ids in respi:
                        ret += 2+idscore
                    else:
                        ret += 0.5+idscore
                dicti[whole] = round(ret * 1.3*(n[1]-1))

        ordl = sorted(dicti.items(), key=lambda x: x[1], reverse=True)
        return ordl, dicti

# -----END LOOKUP BLOCK-----



# -----BEGIN FOOTER BLOCK-----

if __name__=='__main__':
    sql.close()

# -----END FOOTER BLOCK-----

