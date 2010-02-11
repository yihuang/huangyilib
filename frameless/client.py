import urllib2, urllib
url_arg = urllib.quote('hello world')
input_data = 'aaa=bbb&bbb=ccc'
print urllib2.urlopen('http://localhost:8000?'+url_arg, input_data).read()
