find
====

A Python Web Crawler and Search Engine, using MySQL.

It is split up into two parts (crawl.py and find.py).

So far it's not very accessable. I  plan on making a web interface for it, mainly to learn about backend web development (Django).

The search engine is currently quite basic - it orders the sites per query based on the amount of pages that link to them.

It ignores subdomains and it only looks at the default page. This reults in less specific results but a broader range.


Here is the search interface, so far:

![alt text](http://i.imgur.com/ujCKfuR.png)
