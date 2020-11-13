# Тестовое задание на позицию стажера-бекендера<br/>(Test task for the position of intern-backend)

Цель задания – разработать чат-сервер, предоставляющий HTTP API для работы с чатами и сообщениями пользователя.<br/>
(The purpose of the task - to develop a chat server that provides HTTP API to work with chat rooms, and user messages.)<br/><br/>
Задание выполнено на Python + Django + Docker



## Ссылка на задание (Link to original task)
https://github.com/avito-tech/msg-backend-trainee-assignment
    

### Добавить нового пользователя (Add new user)

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username": "user_1"}' \
  http://localhost:9000/users/add
```

Ответ: `id` созданного пользователя или HTTP-код ошибки + описание ошибки.

### Создать новый чат между пользователями (Create new chat with users)

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name": "chat_1", "users": ["<USER_ID_1>", "<USER_ID_2>"]}' \
  http://localhost:9000/chats/add
```

Ответ: `id` созданного чата или HTTP-код ошибки или HTTP-код ошибки + описание ошибки.

Количество пользователей в чате не ограничено.

### Отправить сообщение в чат от лица пользователя (Send message to chat)

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>", "author": "<USER_ID>", "text": "hi"}' \
  http://localhost:9000/messages/add
```

Ответ: `id` созданного сообщения или HTTP-код ошибки + описание ошибки.

### Получить список чатов конкретного пользователя (Take user's chats list)

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user": "<USER_ID>"}' \
  http://localhost:9000/chats/get
```

Ответ: cписок всех чатов со всеми полями, отсортированный по времени создания последнего сообщения в чате (от позднего к раннему). Или HTTP-код ошибки + описание ошибки.

### Получить список сообщений в конкретном чате (Take messages from chat)

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>"}' \
  http://localhost:9000/messages/get
```

Ответ: список всех сообщений чата со всеми полями, отсортированный по времени создания сообщения (от раннего к позднему). Или HTTP-код ошибки + описание ошибки.


## Запуск приложения (How to run)
   - git clone https://github.com/single7troke/avito-tech-chat-server
   - docker-compose up -d
    