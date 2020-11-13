from django.db import models


class User(models.Model):
	username = models.CharField(max_length=32, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Username: {self.username}"


class Chat(models.Model):
	name = models.CharField(max_length=64, unique=True)
	users = models.ManyToManyField(User)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Chatname: {self.name}"


class Message(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=256)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"message: {self.text}\nuser_id: {self.author}\nchat_id: {self.chat}"

