from . import socketio

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))