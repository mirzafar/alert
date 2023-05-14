import math
import re
from hashlib import md5

from bson import ObjectId
from sanic import response

from core.db import mongo
from core.handlers import BaseAPIView, TemplateHTTPView
from utils.ints import IntUtils
from utils.lists import ListUtils
from utils.strs import StrUtils

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UsersView(BaseAPIView):
    template_name = 'admin/users-list.html'

    async def get(self, request, user):
        context = dict()

        limit = IntUtils.to_int(request.args.get('limit')) or 15
        page = IntUtils.to_int(request.args.get('page')) or 1
        skip = (page - 1) * limit

        filter_obj = {
            'status': 0
        }

        data = await mongo.users.find(filter_obj).sort('_id', -1).skip(skip).limit(limit).to_list(length=None)
        for x in data:
            if x.get('scope'):
                x['roles'] = await mongo.roles.find({'title': {'$in': x['scope']}, 'status': 0}).to_list(length=None)

        context['data'] = data
        context['page'] = page

        total = await mongo.users.count_documents(filter_obj)
        context['_range'] = math.ceil(total / limit)

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)

    async def post(self, request, user):
        first_name = StrUtils.to_str(request.json.get('first_name'))
        last_name = StrUtils.to_str(request.json.get('last_name'))
        middle_name = StrUtils.to_str(request.json.get('middle_name')) or ''
        birthday = StrUtils.to_str(request.json.get('birthday')) or ''
        username = StrUtils.to_str(request.json.get('username'))
        email = StrUtils.to_str(request.json.get('email'))
        iin = StrUtils.to_str(request.json.get('iin')) or ''
        phone_number = StrUtils.to_str(request.json.get('phone_number')) or ''
        password = StrUtils.to_str(request.json.get('password'))
        reply_password = StrUtils.to_str(request.json.get('reply_password'))
        photo = StrUtils.to_str(request.json.get('photo')) or ''
        role_id = StrUtils.to_str(request.json.get('role_id'))
        scope = ListUtils.to_list_of_strs(request.json.get('scope'))

        if username:
            duplicate = await mongo.users.find_one({'username': username, 'status': 0})
            if duplicate:
                return response.json({
                    '_success': False,
                    'message': 'Duplicate: username'
                })
        else:
            return response.json({
                '_success': False,
                'message': 'Required param(s): username'
            })

        if any([
            not first_name,
            not last_name,
        ]):
            return response.json({
                '_success': False,
                'message': 'Required param(s): last_name or first_name'
            })

        if email:
            if not re.fullmatch(email_regex, email):
                return response.json({
                    '_success': False,
                    'message': 'Invalid email'
                })
        else:
            return response.json({
                '_success': False,
                'message': 'Required param(s): email'
            })

        if not scope:
            return response.json({
                '_success': False,
                'message': 'Required param(s): scope'
            })

        if not role_id:
            return response.json({
                '_success': False,
                'message': 'Required param(s): role_id'
            })

        if password and reply_password:
            if password == reply_password:
                passwd_hash = md5()
                passwd_hash.update(password.encode())
                password = passwd_hash.hexdigest()
            else:
                return response.json({
                    '_success': False,
                    'message': 'Password does not match'
                })
        else:
            return response.json({
                '_success': False,
                'message': 'Required param(s): password'
            })

        if phone_number:
            if not any([(phone_number.startswith('87') and len(phone_number) == 11),
                        (phone_number.startswith('+7') and len(phone_number) == 12)]):
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

        await mongo.users.insert_one({
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'birthday': birthday,
            'iin': iin,
            'photo': photo,
            'phone_number': phone_number,
            'role_id': role_id,
            'username': username,
            'password': password,
            'email': email,
            'scope': scope,
            'status': 0
        })

        return response.json({
            '_success': True
        })
