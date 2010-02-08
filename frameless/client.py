import urllib2, urllib
url_arg = urllib.quote(raw_input())
input_data = urllib.quote('aaa\nbbb\nccc\n')
print urllib2.urlopen('http://localhost:8000?'+url_arg, input_data).read()
