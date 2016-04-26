Tornado Chat

Примеры запросов

Запрос: curl 'localhost:8888/messages/last_conversations?user_id=2&count=3' | json_pp

Ответ:

{
   "messages" : [
      {
         "text" : "hi 3",
         "timestamp" : "2016-04-26T16:39:30",
         "id" : 5
      },
      {
         "id" : 4,
         "text" : "GOGO",
         "timestamp" : "2016-04-26T03:58:15"
      },
      {
         "id" : 3,
         "text" : "lalki",
         "timestamp" : "2016-04-26T03:55:08"
      }
   ]
}

Запрос:
curl 'localhost:8888/messages/new?user_id=2&count=2' | json_pp

Ответ:

{
   "messages" : [
      {
         "timestamp" : "2016-04-26T02:48:26",
         "id" : 1,
         "text" : "hi"
      },
      {
         "id" : 3,
         "timestamp" : "2016-04-26T03:55:08",
         "text" : "lalki"
      }
   ]
}

Запрос:
curl 'localhost:8888/messages/send' -d 'user_id=3&receiver=2&text=hi23'

Ответ:
6

