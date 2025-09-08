# Dnevnik
Приложение для ведения электронного журнала преподавателя с функциями учета посещаемости, управления группами и студентами, а также ведения домашних заданий

## Функционал
- Управление группами и студентами (добавление, удаление)
- Ведение журнала посещаемости по группам
- Домашние задания с редактором Markdown (для преподавателей) и рендером + возможностью отправить ссылку на GitHub (для студентов)
- Контроль сроков публикации и дедлайна заданий
- Хранение паролей в базе в хэшированном виде с bcrypt

## Запуск
Для начала работы надо применить миграции
```python
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
И создать пользователей и админа
```python
flask create-user teacher1 secretpassword teacher
flask create-user student1 secretpassword student
flask create-user admin adminsecretpassword admin
```