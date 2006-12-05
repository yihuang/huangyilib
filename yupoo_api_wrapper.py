from xml.dom import minidom
from urllib2 import urlopen

API_KEY = 'put your api key here'
base_url = 'http://www.yupoo.com/api/rest/?%s'
src_url = 'http://photo%(host)s.yupoo.com/%(dir)s/%(filename)s.jpg'
link_url = 'http://www.yupoo.com/photos/view?id=%(id)s'

def args( **kw ):
    return '&'.join( [ '%s=%s'%(k,v) for k,v in kw.iteritems()])

def call(**kw):
    url = base_url % args( api_key=API_KEY, **kw )
    f = urlopen( url )
    xmldoc = minidom.parse( f )
    return xmldoc.firstChild.firstChild

def photos_search( tags, **kw ):
    result = call( method='yupoo.photos.search', tags=tags, **kw )
    pics = []
    for n in result.firstChild.childNodes:
        picurl = src_url % dict(
                        host=n.getAttribute('host'),
                        dir=n.getAttribute('dir'),
                        filename=n.getAttribute('filename'))
        linkurl = link_url % dict( id=n.getAttribute('id') )
        pics.append( (picurl,linkurl) )
    return pics

if __name__=='__main__':
    urls = photos_search('mm',per_page=50)
    assert len(urls)<=50
    for link,src in urls:
            print link,src