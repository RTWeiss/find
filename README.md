find
====

Try it here:
[find.noahingham.com](http://noahingham.com/find/search) (Currently down; I was hosting it on a desktop computer that I don't have access to anymore.)

A Python Web Crawler and Search Engine, using MySQL.

It is split up into three parts, the crawler (crawl.py), searcher (find.py) and  a web interface (search and html.html).

The web server uses Common Gateway Interface (CGI) to run Python from the webpage.

There are two main SQL tables used. One for the URLs, each with a unique ID, a boolean value indincating whether they have been parsed, the IDs of URLs that link to the page, and the description of the page (meta content, title, headers and the first paragraph).

The second one, the Search database, is a list of words. Each word has an array of IDs of the pages containing the word. When a quary is made, all the relevant URLs are retrieved and ranked.
The ranking is based on the number of times the keyword appears in the page (favouring titles and headers) and the number of URLs that link to the page, favouring URLs that also contain the particual keyword.
All the details (title and description) of the URL are shown in the results.

Currently, the crawler ignores subdomains and directories, only looks at the default page. This leads to less specific results but a broader range.
The only exceptions are Wikipedia and Tumblr.

Here is the CLI search interface, so far (see link for web interface):

![alt text](http://i.imgur.com/ujCKfuR.png)
