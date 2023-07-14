# Тестовое задание "Бот Напоминаний"

Краткое описание: есть GoogleSheets, который мониторит менеджер. А именно он расписывает напоминания для указанных сотрудников. Нужно сделать бота, который будет высылать сообщения сотрудникам о том, что они должны сделать, и в зависимости от их реакций отправлять все это менеджеру.

## 1 час реализации

Кратко о том, что было проделано:
- Был зарезервирован бот https://t.me/burgerkit_test_job_bot,
- Далее создан GoogleSheets, где будут хранится наши напоминания https://docs.google.com/spreadsheets/d/1_Jmq57sLQGqKlmTGi-kdbyIrieaTgD01ZflsaZtDD4k/edit#gid=0,
- Потом с помощью SheetyAPI я подключил связь между кодом и эксэлькой,
- Подключил библиотеки и сделал кнопки, которые будут выводится,
- Бот берет только те данные, которые не входят в список [Done, Not done, Ignored], т.е. проделанные, непроделанные и игнорированные. И если пользователь за отведенное время данный пользователь не отреагировал, то придет сообщение менеджеру об этом.

Чего не хватает и что не так:
- Программа постоянно "выстреливает" сообщениями об одних и тех же напомнинаниях. И тут не хватает статуса "Send"(отправленный), т.е. по этому признаку мы отправим кнопки только один раз пользователю
- Также не реализована реакция на нажатие кнопок "Да" и "Нет". Вот это тоже остается проделать.

## 20 минут дополнительной реализации

Было проделаны вышеописанные недостатки, также были найденные баги(забыл некоторые вещ поменять) в виде того что дата не бралась именно с того места, а была статична.
К сожалению, бесплатное количество использования APISheety у меня закончилось, поэтому пришлось полагаться только на интуицию и проделать остальную работу без тестов. В целом код старый был протестен и я думаю в целом данный проект работает😉
