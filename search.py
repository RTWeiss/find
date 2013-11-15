#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, cgi
cgitb.enable()

print("Content-Type: text/plain;charset=utf-8")
print('')
form = cgi.FieldStorage()
name = form.getvalue('url')
print('find')
import crawler.find
crawler.find.look(name)
crawler.find.sql.close()
