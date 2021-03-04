from waitress import serve

from api.wsgi import application

if __name__ == '__main__':
    serve(application, port='8000', threads=10, connection_limit=200, channel_timeout=200, outbuf_overflow=10485760, inbuf_overflow=5242880, max_request_header_size=2621440, recv_bytes=8192)