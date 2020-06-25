import eventlet

from src.main.CommunicationLayer import WebService
from eventlet import wsgi

if __name__ == "__main__":
   # WebService.app.run()
    WebService.socket.run(WebService.app)
   #  wsgi.server(eventlet.listen(('', 5000)), WebService.app)

