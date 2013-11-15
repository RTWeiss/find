find
====

A Python Web Crawler and Search Engine, using MySQL.

It is split up into two parts (crawl.py and find.py).

The web interface is currently very basic.
I'll link to it once it works as intened.

The search engine's sorting algorithm is not very complicated - it orders the sites per query based on the amount of pages that link to them.
I'll fix it when it's website looks better.

The crawler ignores subdomains and it only looks at the default page. This leads to less specific results but a broader range.


Here is the CLI search interface, so far:

![alt text](http://i.imgur.com/ujCKfuR.png)
