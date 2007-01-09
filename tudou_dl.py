import sys
import re
import urllib2

info_url = 'http://www.tudou.com/player/i.php'
standard_url_tmp = 'http://www.tudou.com/programs/view/%s/'
querystring_tmp = 'id=%s&retry=%s'
iid_re = re.compile('var iid=(\d+)', re.M)
input_url_re = re.compile(r'(?:http://)?(?:www\.)?tudou\.com/programs/view/(\w+)/?')

# get the input url
if len(sys.argv)<2 or sys.argv[1] in ['-h', '--help']:
    print '''usage: tudou_dl.py url'''
    sys.exit(1)
url = sys.argv[1]

# Verify the input url and build a standard one
match = input_url_re.match(url)
if not match:
    print 'please input a correct url.'
    sys.exit(1)
url = standard_url_tmp % match.group(1)

print 'fetching the page', url, '...'
page = urllib2.urlopen(url).read()

# get the iid
print 'analoging current page...'
match = iid_re.search(page)
if not match:
    print 'can\'t find the iid in this page'
    sys.exit(1)
iid = match.group(1)

# construct the querystring, and post to info_url
querystring = querystring_tmp % (iid, 0)
print 'fetching the infos...'
real_url = urllib2.urlopen(info_url, querystring).read()
print 'the real video url is', real_url
