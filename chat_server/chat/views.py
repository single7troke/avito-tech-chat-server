import datetime
import json

from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def user_add(request):
	if request.method != "POST":
		return HttpResponse('405 Method Not Allowed', status=405)

	data = json.loads(request.body.decode())
	username = data["username"]
	if not username.strip():
		return HttpResponse('username cannot be empty')
	try:
		new_user = User.objects.create(username=username)
		new_user.save()
	except IntegrityError:
		return HttpResponse(f"User with username: {data['username']} already exists")
	return JsonResponse({"id": new_user.id})


@csrf_exempt
def chat_add(request):
	if request.method != "POST":
		return HttpResponse('405 Method Not Allowed', status=405)

	data = json.loads(request.body.decode())
	chat_name = data["name"]
	users = data["users"]
	if not chat_name.strip():
		return HttpResponse('chat name cannot be empty')
	try:
		chat = Chat.objects.create(name=chat_name)
		chat.save()
	except IntegrityError:
		chat = Chat.objects.get(name=chat_name)
	for i in users:
		try:
			user = User.objects.get(id=i)
			chat.users.add(user)
		except User.DoesNotExist:
			pass
	return JsonResponse({"id": chat.id})


@csrf_exempt
def users_chats(request):
	if request.method != "POST":
		return HttpResponse('405 Method Not Allowed', status=405)

	data = json.loads(request.body.decode())
	user_id = data["user"]
	try:
		user = User.objects.get(id=user_id)
		chats = user.chat_set.all()
		user_data = []
		for chat in chats:
			last_message = Message.objects.all().filter(chat_id=chat.id).last()
			if last_message:
				user_data.append([{"id": chat.id, "name": chat.name, "created_at": f"{chat.created_at:%Y-%m-%d %H:%M:%S}"},
									str(last_message.created_at)])
			else:
				user_data.append([{"id": chat.id, "name": chat.name, "created_at": f"{chat.created_at:%Y-%m-%d %H:%M:%S}"},
									str(datetime.datetime(1, 1, 1, 0, 0, 0, 0))])
		return JsonResponse({"chats": [x[0] for x in sorted(user_data, key=lambda x: x[-1], reverse=True)]})
	except User.DoesNotExist:
		return HttpResponse(f"User with id: {user_id} does not exist")


@csrf_exempt
def message_add(request):
	if request.method != "POST":
		return HttpResponse('405 Method Not Allowed', status=405)

	data = json.loads(request.body.decode())
	chat_id, user_id, text = data["chat"], data["author"], data["text"]
	if not chat_id.strip() or not user_id.strip() or not text.strip():
		HttpResponse("chat, author or text cannot be empty")
	try:
		chat = Chat.objects.get(id=chat_id)
		user = User.objects.get(id=user_id)
		message = Message.objects.create(chat=chat, author=user, text=text)
		message.save()
		return HttpResponse(message.id)
	except Chat.DoesNotExist:
		return HttpResponse(f"Chat with id: {chat_id} does not exist")
	except User.DoesNotExist:
		return HttpResponse(f"User with id: {user_id} does not exist")


@csrf_exempt
def chats_messages(request):
	if request.method != "POST":
		return HttpResponse('405 Method Not Allowed', status=405)

	data = json.loads(request.body.decode())
	chat_id = data["chat"]
	if not chat_id.strip():
		HttpResponse("Chat id cannot be empty")
	try:
		chat = Chat.objects.get(id=chat_id)
		messages = Message.objects.all().filter(chat_id=chat.id)
		return JsonResponse({"messages": [{"id": x.id,
											"chat": x.chat_id,
											"author": x.author_id,
											"text": str(x.text),
											"created_at": f"{x.created_at:%Y-%m-%d %H:%M:%S}"} for x in messages]},
											json_dumps_params={'ensure_ascii': False})
	except ValueError:
		return HttpResponse("Incorrect chat id")
	except Chat.DoesNotExist:
		return HttpResponse(f"Chat with id: {chat_id} does not exist")

