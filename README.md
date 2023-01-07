<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<h1 align="center"> Fjord API</h1>

<p align="center">
  <img src="https://i.imgur.com/TFSvRC3.png" alt="Welcome Logo" width="800">
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<div align="center">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg"/>
    <img src="https://forthebadge.com/images/badges/winter-is-coming.svg"/>
    <img src="https://forthebadge.com/images/badges/powered-by-overtime.svg"/>
</div>
<div align="center">
    <img src="https://forthebadge.com/images/badges/made-with-markdown.svg"/>
    <img src="http://forthebadge.com/images/badges/built-with-love.svg"/>
    <img src="https://forthebadge.com/images/badges/certified-elijah-wood.svg"/>
</div>

<div align="center">
    <h4>
        <img width="13%" src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
        <img width="26%" src="https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg"/>
    </h4>
</div>


<div align="center">
    <h4>
        <a href="https://docs.python.org/3/whatsnew/3.10.html">
            <img src="https://img.shields.io/badge/Made%20with-Python%203.10-1f425f.svg?logo=python"/>
        </a>
        <a href="https://github.com/pre-commit/pre-commit">
            <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat"/>
        </a>
        <a href="">
            <img src="https://img.shields.io/badge/contributions-welcome-orange.svg"/>
        </a>
        <a href="">
            <img src="https://img.shields.io/badge/PRs-welcome-orange.svg?style=shields"/>
        </a>
    </h4>
</div>
<div align="center">
    <h4>
        <a href="https://github.com/psf/black">
            <img src="https://img.shields.io/badge/code%20style-black-000000.svg"/>
        </a>
        <a href="http://mypy-lang.org/">
            <img src="http://www.mypy-lang.org/static/mypy_badge.svg"/>
        </a>
        <a href="https://pycqa.github.io/isort/">
            <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"/>
        </a>
        <a href="">
            <img src="https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg"/>
        </a>
    </h4>
</div>

<div align="center">

[**Description**](#description) •
[**Quickstart**](#quickstart) •
[**Project Structure**](#project-structure) •
[**Stack**](#stack)

</div>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 align="center" id="description">📖 Description</h2>

The main goal of this project is to conveniently and quickly receive translations of texts.

You can get translations and detect the language of the input text, both individually (single) and for the whole document (Google Sheet).

Also, the project allows you to get valid proxies through separate endpoints.

**Available languages** for translation: `English`, `German`, `Italian`, `Ukrainian`, `Norwegian` and `Japanese`.

**Available providers** for translation: `Google Translate`, `Libre Translate`, `MyMemory` and `DeepL`.

The project is completely asynchronous, has an admin panel, integration with Mongo, Postgres and Redis.

If necessary, you can download the translations attached to the original Google sheet through a separate endpoint.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 align="center" id="quickstart">⚡️ Quickstart</h2>

* Clone the repo and navigate to the root folder.

* Create and activate a python3 virtualenv via your preferred method or with:

	```bash
	make ve
	```

	* For remove virtualenv:

	```bash
	make clean
	```

* If you setup virtualenv on your own - install the dependencies. Run:

	```bash
	pip install -r requirements.txt
	```

* Install pre-commit hooks to ensure code quality checks and style checks:

	```bash
	make install_hooks
	```

	* You can also use these commands during dev process:

		* To run **mypy** checks:

			```bash
			make types
			```

		* To run **flake8** checks:

			```bash
			make style
			```

		* To run **black** checks:

			```bash
			make format
			```

		* To run together:

			```bash
			make lint
			```

* Replace `.env.example` with real `.env`, changing placeholders

	```
	CURRENT_ENV=<staging|rc|production>

    SECRET_KEY=changeme

    REDIS_HOST=<redis-host>
    REDIS_PASSWORD=<redis-password>
    REDIS_PORT=<redis-port>
    REDIS_DB=<redis-db>
    REDIS_KEY=<redis-key>

    MONGO_HOST=<mongo-host>
    MONGO_DB=<mongo-db>
    MONGO_USER=<mongo-user>
    MONGO_PASSWORD=<mongo-password>
    MONGO_TASKS_COLLECTION=<mongo-tasks-collection>
    MONGO_USERS_COLLECTION=<mongo-users-collection>

    POSTGRES_HOST=<postgres-host>
    POSTGRES_PORT=<postgres-port>
    POSTGRES_DB=<postgres-db>
    POSTGRES_USER=<postgres-user>
    POSTGRES_PASSWORD=<postgres-password>

    TG_BOT_TOKEN=<tg-bot-token>
    TG_CHAT_ID=<tg-chat-id>

    MYMEMORY_EMAIL=<email-for-mymemory>
    DETECT_LANGUAGE_API_KEY=<detect-language-api-key>

    TCP_CONNECTOR_LIMIT=<tcp-connector-limit>
    ASYNC_TRANSLATION_TASKS_NUM=<async-translation-tasks-num>

    MAX_CONCURRENT_TASKS=<max-concurrent-tasks>
    RUN_BACKGROUND_TASKS=<1|0>
    SCHEDULER_TASK_INTERVAL=<seconds-interval>

    GRAYLOG_HOST=<graylog-host>
    GRAYLOG_INPUT_PORT=<graylog-port>

    SENTRY_DSN=<sentry-dsn>
	```

* Export path to Environment Variables:

	```bash
	export PYTHONPATH='.'
	```

* Run following commands to make migrations anc create admin user:

	```bash
	piccolo migrations forwards user
    piccolo user create
	```

* Start the Fjord API App:

	* Run server with test settings:

		```bash
		 make runserver-test
		```

	* Run server with dev settings:

		```bash
		 make runserver-dev
		```
	* Run server with prod settings:

		```bash
		 makerunserver-prod
		```

	You will see something like this:

	```console
	$ uvicorn main.app:app --reload
	INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
	INFO:     Started reloader process [28720]
	INFO:     Started server process [28722]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	```

	<details markdown="1">
	<summary>About the command <code>uvicorn main:app --reload</code>...</summary>

	The command `uvicorn main.app:app` refers to:

	* `main`: the file `main.py` (the Python "module").
	* `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
	* `--reload`: make the server restart after code changes. Only do this for development.

	</details>

* If everything is fine, check this endpoint:

	```bash
	curl -X "GET" http://host:port/api/v1/status
	```

	Expected result:

	```json
	{
	  "success": true,
	  "version": "<version>",
	  "message": "Fjord API"
	}
	```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 align="center" id="project-structure">🛠️ Project Structure</h2>

This shows the structure of the Ataman App.

```
fjord-api
├── main                                # primary app folder
│   ├── api                             # this houses for API packages
│   │   ├── routes                      # this is where all the routes live
│   │   │   ├── __init__.py             # empty init file to make the routes folder a package
│   │   │   ├── auth.py                 # module with auth endpoint
│   │   │   ├── proxies.py              # module with proxy utils endpoint
│   │   │   ├── status.py               # module with health check endpoint
│   │   │   ├── tasks.py                # module with endpoints to handle translation task
│   │   │   └── translation.py          # module with translation utils endpoint
│   │   ├── __init__.py                 # empty init file to make the api folder a package
│   │   ├── background.py               # file containing all background tasks
│   │   └── routes.py                   # manages all routers in the project
│   ├── apps                            # this houses for Piccolo settings + template endpoints
│   │   ├── home                        # settings for Home App
│   │   │   ├── piccolo_migrations      # this houses for postgres migrations
│   │   │   │   └── __init__.py         # empty init file to make the piccolo_migrations folder a package
│   │   │   ├── templates               # jinja temolates for Home App
│   │   │   │   └── index.html.jinja    # home page template
│   │   │   ├── __init__.py             # empty init file to make the home folder a package
│   │   │   ├── endpoints.py            # endpoint settings for home page
│   │   │   └── piccolo_app.py          # general piccolo app config
│   │   └── __init__.py                 # empty init file to make the apps folder a package
│   ├── const                           # store all the consts necessary for the application
│   │   ├── __init__.py                 # empty init file to make the const folder a package
│   │   ├── common.py                   # common consts
│   │   ├── proxies.py                  # consts for proxy services
│   │   └── translator.py               # consts for translation services
│   ├── core                            # this is where the configs live
│   │   ├── settings                    # home for all setting files
│   │   │   ├── __init__.py             # empty init file to make the settings folder a package
│   │   │   ├── app.py                  # base application settings
│   │   │   ├── base.py                 # contains base app setting class and app envs
│   │   │   ├── development.py          # development app settings
│   │   │   ├── production.py           # production app settings
│   │   │   └── test.py                 # test app settings
│   │   ├── __init__.py                 # empty init file to make the config folder a package
│   │   ├── config.py                   # sample config file
│   │   ├── dependencies.py             # auth dependency
│   │   ├── exceptions.py               # app exception handlers
│   │   ├── integrations.py             # module for project 3rd parties services
│   │   ├── logging.py                  # module configuration custom logger
│   │   └── security.py                 # auth security utils
│   ├── db                              # this is where the repositories logic live
│   │   ├── models                      # postgres models
│   │   │   ├── __init__.py             # empty init file to make the models folder a package
│   │   │   └── postgres.py             # contains postgres models
│   │   ├── repositories                # home for all repository files
│   │   │   ├── __init__.py             # empty init file to make the repositories folder a package
│   │   │   ├── base.py                 # contains base repositories classes
│   │   │   ├── proxies.py              # repository to manipulate with proxies in Redis
│   │   │   ├── tasks.py                # repository to manipulate with translation tasks from Mongo collection
│   │   │   └── users.py                # repository to manipulate with users from Mongo collection
│   │   ├── __init__.py                 # empty init file to make the repositories folder a package
│   │   ├── clients.py                  # provide client for MongoDB, Elasticsearch, etc.
│   │   ├── connections.py              # process Postgres database connections
│   │   └── errors.py                   # module for custom database errors
│   ├── schemas                         # this is where the schemas live
│   │   ├── __init__.py                 # empty init file to make the schemas folder a package
│   │   ├── auth.py                     # users item schema
│   │   ├── common.py                   # contains common schemas
│   │   ├── notifier.py                 # notifier error schema
│   │   ├── proxies.py                  # proxy item schema
│   │   ├── status.py                   # health check schema
│   │   ├── tasks.py                    # schemas for translation tasks
│   │   └── translation.py              # single translation/detection schemas
│   ├── services                        # this is where services live
│   │   ├── common                      # home for all main services
│   │   │   ├── __init__.py             # empty init file to make the common folder a package
│   │   │   ├── proxy.py                # proxy pool service
│   │   │   └── translation.py          # service for single translation/detection
│   │   ├── extra                       # home for all extra services
│   │   │   ├── proxynator.py           # module to gather fresh proxies
│   │   │   │   ├── crawlers            # crawlers logic
│   │   │   │   │   ├── public          # public crawlers
│   │   │   │   │   │   ├── __init__.py # empty init file to make the public folder a package
│   │   │   │   │   │   └── *           # different crawlers
│   │   │   │   │   ├── __init__.py     # empty init file to make the crawlers folder a package
│   │   │   │   │   └── base.py         # abstract crawler class with all main proxy getter logic
│   │   │   │   ├── __init__.py         # empty init file to make the proxynator folder a package
│   │   │   │   └── main.py             # fetching new fresh proxies and add them to Redis
│   │   │   ├── translator.py           # module with translation providers
│   │   │   │   ├── providers           # providers logic
│   │   │   │   │   ├── __init__.py     # empty init file to make the crawlers folder a package
│   │   │   │   │   ├── base.py         # abstract provider class with all main translation getter logic
│   │   │   │   │   ├── deepl.py        # logic to get translation from DeepL provider
│   │   │   │   │   ├── google.py       # logic to get translation from Google Translate provider
│   │   │   │   │   ├── libre.py        # logic to get translation from LibreTranslate provider
│   │   │   │   │   └── mymemory.py     # logic to get translation from MyMemory provider
│   │   │   │   ├── __init__.py         # empty init file to make the proxynator folder a package
│   │   │   │   └── main.py             # general logic to get single/multiple translations
│   │   │   ├── __init__.py             # empty init file to make the extra folder a package
│   │   │   ├── auth.py                 # handles users auth
│   │   │   ├── errors.py               # handles async sessions and possible errors
│   │   │   └── notifier.py             # service for sending notifications to Telegram
│   │   ├── __init__.py                 # empty init file to make the services folder a package
│   │   ├── executor.py                 # translation task executor
│   │   ├── scheduler.py                # translation task scheduler
│   │   └── tasks.py                    # service to handle translation tasks
│   ├── static                          # contains static files
│   └── *.css, *.js, *ico               # different static files like .css, .js or images
│   ├── utils                           # this is where the utils live
│   │   ├── __init__.py                 # empty init file to make the utils folder a package
│   │   ├── common.py                   # contains common utils
│   │   ├── proxies.py                  # utils to check/convert proxies
│   │   └── tasks.py                    # includes tools for generating random IDs and form error messages
│   ├── __init__.py                     # empty init file to make the main folder a package
│   └── app.py                          # main file where the fastAPI() class is called
├── .env                                # env file containing app variables
├── .env.test                           # env file containing app test variables
├── .pre-commit-config.yaml             # describes what repositories and hooks are installed
├── docker-compose.yml                  # docker-compose file
├── Dockerfile                          # prod Dockerfile
├── Makefile                            # shell commands for convenient project use
├── piccolo_conf.py                     # piccolo config (app registry, engine)
├── pyproject.toml                      # pep-518 compliant config file
├── requrements-ci.txt                  # pinned ci dependencies
├── requirements-prod.txt               # pinned prod dependencies
├── requirements.txt                    # pinned app dependencies
├── setup.cfg                           # linter config file
└── version.py                          # app version file                      # app version file
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 align="center" id="stack">📚 Stack</h2>

- <img width=3% src="https://cdn.worldvectorlogo.com/logos/fastapi.svg"> <b><a href="https://fastapi.tiangolo.com/">&nbsp;FastAPI</a></b>
- <img width=3% src="https://upload.wikimedia.org/wikipedia/commons/0/00/Kubernetes_%28container_engine%29.png"> <b><a href="https://github.com/kubernetes-client/python/">&nbsp;Kubernetes</a></b>
- <img width=3% src="https://docs.aiohttp.org/en/v3.7.4/_static/aiohttp-icon-128x128.png"> <b><a href="https://docs.aiohttp.org/en/v3.7.4/">&nbsp;aiohttp</a></b>
- <img width=3% src="https://avatars.githubusercontent.com/u/1529926?s=200&v=4"> <b><a href="https://aioredis.readthedocs.io/en/latest/">&nbsp;aioredis</a></b>
- <img width=3% src="https://avatars.githubusercontent.com/u/45742130?v=4"> <b><a href="https://piccolo-orm.com/">&nbsp;Piccolo</a></b>
- <img width=3% src="https://infinapps.com/wp-content/uploads/2018/10/mongodb-logo.png"> <b><a href="https://pymongo.readthedocs.io/">&nbsp;PyMongo</a></b>
- <img width=3% src="https://quintagroup.com/cms/python/images/jinja2.png/@@images/919c2c3d-5b4e-4650-943a-b0df263f851b.png"> <b><a href="https://jinja.palletsprojects.com/en/3.1.x/">&nbsp;Jinja</a></b>
- <img width=3% src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2048px-Python-logo-notext.svg.png"> <b><a href="https://pydantic-docs.helpmanual.io/">&nbsp;Pydantic</a></b>
- <img width=3% src="https://user-images.githubusercontent.com/11155743/56979626-e8f80680-6b82-11e9-9a54-9289d3289e45.png"> <b><a href="https://www.starlette.io/">&nbsp;Starlette</a></b>
- <img width=3% src="https://raw.githubusercontent.com/tomchristie/uvicorn/master/docs/uvicorn.png"> <b><a href="https://www.uvicorn.org/">&nbsp;Uvicorn</a></b>
- <img width=3% src="https://cdn.worldvectorlogo.com/logos/graylog.svg"> <b><a href="https://graypy.readthedocs.io/en/latest/">&nbsp;graypy</a></b>
- <img width=3% src="https://cdn.worldvectorlogo.com/logos/sentry-3.svg"> <b><a href="https://docs.sentry.io/platforms/python/">&nbsp;Sentry</a></b>
- <img width=3% src="https://cdn.worldvectorlogo.com/logos/gunicorn.svg"> <b><a href="https://gunicorn.org/">Gunicorn</a></b>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 align="center" id="contributors">✨ Contributors</h2>


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table align="center">
  <tr>
   <td align="center"><a href="https://github.com/Russkiy-Voyennyy-Korabl-Idi-Nakhuy"><img src="https://avatars.githubusercontent.com/u/43554620??v=4?s=200" width="200px;" alt="Jack Shendrikov"/><br/><sub><b>👑 Jack Shendrikov 👑</b></sub></a></td>
  </tr>
</table>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<div align="center">✨ 🍰 ✨</div>
