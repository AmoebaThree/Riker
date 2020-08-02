import systemd.daemon
import redis
import os
import http.server
import socketserver

root_dir = '/home/pi/zoidberg-deploy/riker/www/'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=root_dir, **kwargs)


def serve():
    with socketserver.TCPServer(("", 7900), Handler) as httpd:
        httpd.serve_forever()


def execute():
    print('Startup')

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)

    r.publish('services', 'riker.on')
    systemd.daemon.notify('READY=1')
    print('Startup complete')

    try:
        serve()
    except:
        r.publish('services', 'riker.off')
        print('Goodbye')


if __name__ == '__main__':
    execute()
