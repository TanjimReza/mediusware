
## Task Manager with REST API

A brief description of what this project does and who it's for


## Run Locally

Clone the project 

```python
  git clone https://github.com/TanjimReza/mediusware.git
```

Go to the project directory

```python
  cd mediusware
```

Install dependencies (Create VirtualEnv First)

```python
  pip install -r requirements.txt
```

Create a Postgres Database and fill-up the corresponding credentials in `.env` file in the root directory.

```python
  SECRET_KEY=SecretKeyHere
  DEBUG=True
  DATABASE_NAME=tanjimtaskdb
  DATABASE_USER=postgres
  DATABASE_PASSWORD=tanjim
  DATABASE_HOST=localhost
  DATABASE_PORT=5432
```

Make Migrations
```python
  python manage.py migrate
```



Import Database from `alldata.json`
```python
  python manage.py loaddata alldata.json
```

Run the server
```python
  python manage.py runserver
```

## Demo Users

#### Django Admin Login

```http
  localhost/admin/
```

| Username | password     | Email                |
| :-------- | :------- | :------------------------- |
| `admin` | `tanjim` | `admin@admin.com` |


#### Custom User login

```http
  localhost/login/
```

| Email | password     |
| :-------- | :------- |
| `user-1@users.com` | `tanjim` |
| `user-2@users.com` | `tanjim` |
| `user-2@users.com` | `tanjim` |



## API Reference

#### Task List Create

```http
  GET /api/tasks/
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `None` | `None` | List All Task |


```http
  GET /api/tasks/
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | Show task details |