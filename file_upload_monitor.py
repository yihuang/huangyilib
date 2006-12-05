from paste.progress import *
import time

upload_page = '''
<html>
    <head>
        <script type="text/javascript">
            // Tested with Opera 9.01, Firefox beta 2 on Linux, should
            // work with IE 6+

            poller = false;
            busy = false;
            http = false;

            function getstats() {
                // Get our XMLHttpRequest object and submit request for stats
                if(!busy){
                    http = false;
                    if(window.XMLHttpRequest) {
                        http = new XMLHttpRequest();
                    }
                    else if(window.ActiveXObject) {
                        try {
                            http = new ActiveXObject("Msxml2.XMLHTTP");
                        } catch (e) {
                            try {
                                http = new ActiveXObject("Microsoft.XMLHTTP");
                            } catch (e) {}
                        }
                    }
                    if(!http) {
                        alert("We're uploading the file, but your browser isn't letting us use AJAX.");
                        document.getElementById('upload_stat').innerHTML='Not available.';
                        return false;
                    }

                    busy = true;
                    http.onreadystatechange = update_stat;
                    http.open("GET", "/report", true);
                    http.send(null);
                }
            }

            function update_stat(){
                var result;
                // Handles the request for stats.
                if(http.readyState == 4){
                    if(http.status != 200){
                       document.getElementById('upload_stat').innerHTML='Stats unavailable. Wait for it.';
                        clearInterval(poller);
                    }else{
                        result = eval(http.responseText)
                        var current = result[result.length-1]
                        received = current.bytes_received
                        size = current.content_length
                        document.getElementById('upload_stat').innerHTML=100*received/size + "%";
                        if(http.responseText.indexOf('No active transfers!') != -1){
                            clearInterval(poller);
                        }
                    }
                }
                busy = false;
            }
            function start_stat(){
                // Hides our upload form and displays our stats element.
                poller = setInterval("getstats()", 2000);
                document.getElementById('upload_stat').style.display = 'block';
                document.getElementById('upload_form').style.display = 'none';
            }
        </script>
    </head>
    <bod>
        <!-- Our form will call the polling system for stats when it's submitted, as well as start the uploading of the file. -->
        <h1>File upload with progress bar</h1>
        Choose your files:<br/>
        <form class="upload_form" action="" method="post" enctype="multipart/form-data" onsubmit="start_stat()">
            <input type="file" name="myFile"/>
            <input type="submit" value="Upload File"/>
        </form>
        <!-- This is where we'll be putting our statistics. It's hidden to start off. -->
        <div id="upload_stat" style="display:none;">Connecting...</div>
    </body>
</html>'''

def FileUploadApp(environ, start_response):
    total = environ.get('CONTENT_LENGTH')
    if total:
        body = '''
        <html><head><title>Upload Succed!</title></head>
        <body><h5>%s bytes upload succed!</h5></body></html>
        ''' % total
    else:
        body = upload_page

    start_response('200 OK', [('Content-Type','text/html'),
                              ('Content-Length',len(body))])
    return [body]

class FileUploader(object):
    def __init__(self, app):
        self.chunk_size = 4096
        self.delay = 1
        self.progress = True
        self.app = app
    def __call__(self, environ, start_response):
        size = 0
        total  = environ.get('CONTENT_LENGTH')
        if total:
            remaining = int(total)
            while remaining > 0:
                if self.progress:
                    print "%s of %s remaining" % (remaining, total)
                if remaining > 4096:
                    chunk = environ['wsgi.input'].read(4096)
                else:
                    chunk = environ['wsgi.input'].read(remaining)
                if not chunk:
                    break
                size += len(chunk)
                remaining -= len(chunk)
                if self.delay:
                    time.sleep(self.delay)
        print "bingles"
        return self.app(environ, start_response)

if __name__ == '__main__':
    from paste.httpserver import serve
    from paste.urlmap import URLMap
    from paste.auth.basic import AuthBasicHandler
    realm = 'Test Realm'
    def authfunc(environ, username, password):
        return username == password

    map = URLMap({})
    ups = UploadProgressMonitor(map, threshold=1024, timeout=0)
    map['/upload'] = FileUploader(FileUploadApp)
    map['/report'] = UploadProgressReporter(ups)
    serve(AuthBasicHandler(ups, realm, authfunc))