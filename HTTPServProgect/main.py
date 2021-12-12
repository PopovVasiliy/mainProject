from QueueMessageStorage import *
from UserStorage import *
from pathlib import Path
from typing import Any, AsyncIterable, Dict, Iterable
from aiohttp import web
import aiohttp_jinja2
import jinja2

routes = web.RouteTableDef()


async def __to_list(iterable: AsyncIterable[Any]) -> Iterable[Any]:
    return [item async for item in iterable]


@routes.get('/')
async def root(_) -> web.Response:
    raise web.HTTPFound(location='/users')


@routes.get('/users')
@aiohttp_jinja2.template('users.jinja2')
async def get_users(request: web.Request) -> Dict[str, Any]:
    userstorage: AbstractServerUsersStorage = request.app['UserStorage']
    queuemessagestorage: AbstractQueueMessageStorage = request.app['QueueMessageStorage']
    return {'users': userstorage.get_all_users(),
            'queuemessages': queuemessagestorage.get_all_messages()
            }


@routes.post('/users')
async def add_user(request: web.Request) -> web.Response:

    userstorage: AbstractServerUsersStorage = request.app['UserStorage']
    data = dict(await request.post())
    serv_user = ServerUser(data.get('nick_user'), data.get('password_user'), data.get('name_user'))
    userstorage.put_user_to_base(serv_user)
    return web.HTTPFound(location=f'/users')


@routes.get('/messages')
@aiohttp_jinja2.template('users.jinja2')
async def get_messages(request: web.Request) -> Dict[str, Any]:
    userstorage: AbstractServerUsersStorage = request.app['UserStorage']
    queuemessagestorage: AbstractQueueMessageStorage = request.app['QueueMessageStorage']
    return {'users': userstorage.get_all_users(),
            'queuemessages': queuemessagestorage.get_all_messages()
            }


@routes.get('/api/users')
async def get_users_api(request: web.Request) -> web.json_response():
    userstorage: AbstractServerUsersStorage = request.app['UserStorage']
    users = [user.to_json() for user in userstorage.get_all_users()]
    return web.json_response(users)


@routes.get('/api/messages')
async def get_messages_api(request: web.Request) -> web.json_response():
    queuemessagestorage: AbstractQueueMessageStorage = request.app['QueueMessageStorage']
    _messages = [_message.to_json() for _message in queuemessagestorage.get_all_messages()]
    return web.json_response(_messages)


@routes.post('/api/users')
async def post_users_api(request: web.Request) -> web.json_response():

    userstorage: AbstractServerUsersStorage = request.app['UserStorage']
    try:
        data = dict(await request.json())
        serv_user = userstorage.get_user(data.get('nick_user'))
        if serv_user is not None and serv_user.ServerUser.password_user == data.get('password_user'):
            return web.json_response(RequestUser.to_json_OK())
        else:
            return web.json_response(RequestUser.to_json_error())
    except Exception:
        return web.json_response(RequestUser.to_json_error())


@routes.post('/api/messages')
async def set_messages_api(request: web.Request) -> web.json_response():
    queuemessagestorage: AbstractQueueMessageStorage = request.app['QueueMessageStorage']
    userstorage: AbstractServerUsersStorage = request.app['UserStorage']

    try:
        data = dict(await request.json())
        client_command = data.get('command')
        if client_command == 'send_message':

            serv_user_recipient = userstorage.get_user(data.get('user_recipient'))
            if serv_user_recipient is None:
                return web.json_response(RequestUser.to_json_error())

            serv_user_sender = userstorage.get_user(data.get('user_sender'))
            if serv_user_sender is None:
                return web.json_response(RequestUser.to_json_error())

            text_message = data.get('text_message')
            if text_message is None:
                return web.json_response(RequestUser.to_json_error())

            queuemessagestorage.put_message(ServerMessage(datetime.now(), serv_user_recipient, serv_user_sender, text_message))

            return web.json_response(RequestUser.to_json_OK())

        elif client_command == 'get_message':
            serv_user_recipient = userstorage.get_user(data.get('user_recipient'))
            if serv_user_recipient is None:
                return web.json_response(RequestUser.to_json_error())

            _messages = [_message.to_json() for _message in queuemessagestorage.get_messages_recipient(serv_user_recipient)]
            queuemessagestorage.clear_messages(serv_user_recipient)
            return web.json_response(_messages)

    except Exception:
        return web.json_response(RequestUser.to_json_error())


if __name__ == '__main__':

    settings = {
        'host': 'localhost',
        'port': 8080
    }

    app = web.Application()
    user_storage = DatabaseServerUsersStorage(Path('server_users_base.db'))
    app['UserStorage'] = user_storage

    queue_message_storage = DatabaseQueueMessageStorage(Path('queue_messages.db'), user_storage)
    app['QueueMessageStorage'] = queue_message_storage

    templates_directory = Path(__file__).parent.joinpath('templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates_directory)))
    app.add_routes(routes)
    web.run_app(app, host=settings['host'], port=settings['port'])
