import re
from hashlib import md5

from bson import ObjectId
from sanic import response

from core.db import mongo
from core.handlers import BaseAPIView
from utils.lists import ListUtils
from utils.strs import StrUtils

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UsersItemView(BaseAPIView):
    template_name = 'admin/users-item.html'

    async def get(self, request, user, user_id):
        user_id = StrUtils.to_str(user_id)

        filter_obj = {
            '_id': ObjectId(user_id)
        }

        context = dict()

        context['data'] = await mongo.users.find_one(filter_obj)
        context['roles'] = await mongo.roles.find({'status': 0}).to_list(length=None)

        return self.render_template(request=request, **context)

    async def post(self, request, user, user_id):
        user_id = StrUtils.to_str(user_id)
        if not ObjectId.is_valid(user_id):
            return response.json({
                '_success': False,
                'message': 'Invalid user id'
            })

        action = StrUtils.to_str(request.json.get('action'))
        first_name = StrUtils.to_str(request.json.get('first_name'))
        last_name = StrUtils.to_str(request.json.get('last_name'))
        middle_name = StrUtils.to_str(request.json.get('middle_name'))
        birthday = StrUtils.to_str(request.json.get('birthday'))
        username = StrUtils.to_str(request.json.get('username'))
        email = StrUtils.to_str(request.json.get('email'))
        iin = StrUtils.to_str(request.json.get('iin'))
        role_id = StrUtils.to_str(request.json.get('role_id'))
        phone_number = StrUtils.to_str(request.json.get('phone_number'))
        password = StrUtils.to_str(request.json.get('password'))
        reply_password = StrUtils.to_str(request.json.get('reply_password'))
        photo = StrUtils.to_str(request.json.get('photo'))
        scope = ListUtils.to_list_of_strs(request.json.get('scope'))

        set_update = {}
        if action == 'update':
            if first_name:
                set_update['first_name'] = first_name

            if last_name:
                set_update['last_name'] = last_name

            if middle_name:
                set_update['middle_name'] = middle_name

            if birthday:
                set_update['birthday'] = birthday

            if photo:
                set_update['photo'] = photo

            if username:
                duplicate = await mongo.users.find_one(
                    {'username': username, 'status': 0, '_id': {'$ne': ObjectId(user_id)}})
                if duplicate:
                    return response.json({
                        '_success': False,
                        'message': 'Duplicate: username'
                    })
                else:
                    set_update['username'] = username

            if email:
                if not re.fullmatch(email_regex, email):
                    return response.json({
                        '_success': False,
                        'message': 'Invalid email'
                    })

                set_update['email'] = email

            if password:
                if password == reply_password:
                    passwd_hash = md5()
                    passwd_hash.update(password.encode())
                    password = passwd_hash.hexdigest()

                    set_update['password'] = password
                else:
                    return response.json({
                        '_success': False,
                        'message': 'Password does not match'
                    })

            if scope:
                set_update['scope'] = scope

            if role_id:
                set_update['role_id'] = role_id

            if phone_number:
                if (phone_number.startswith('87') and len(phone_number) == 11) or (
                        phone_number.startswith('+7') and len(phone_number) == 12):
                    set_update['phone_number'] = phone_number
                else:
                    return response.json({
                        '_success': False,
                        'message': 'Invalid phone number'
                    })

            if iin:
                if len(iin) != 12:
                    return response.json({
                        '_success': False,
                        'message': 'Invalid iin'
                    })

                set_update['iin'] = iin

            await mongo.users.update_one({'_id': ObjectId(user_id)}, {'$set': set_update})

        elif action == 'delete':
            await mongo.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': -1}})

        return response.json({
            '_success': True
        })
