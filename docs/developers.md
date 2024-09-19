# Developers

This application is developed in python 3 with fastapi. It uses a webhook endpoint at / that received all github webhook events.

The webhook events are filters and converted to a message. See [constants.py](../blob/main/app/contants.py) for the default conversion. After converting the github webhook event to a message the message is send to one or more of the clients for further handling. Depending on the client the message can be processed differenlty.

## Developing

To start the application you first need to install python3 and all dependencies. We assume you have python3 installed. If not see the python3 documentation.

You may want to start a virtual env before proceding, but this is not required. to created a virtual env do the following:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

To install all required dependencies do the following:

```shell
pip install -r requirements-dev.txt
```

After all dependencies have been installed you can start the application:

```shell
fastapi run app/main.py
```

## pre-commit

We recommend using the pre-commit application when developing to standarize the development rules. Pre-commit does not check all things the CI/CD does but it does some.

to enable pre-commit do the following:

```shell
pre-comit install
```

Now, every time you do a `git commit` the pre-commit hooks will do validation of your files. Note: it does not run pyright.

## formatting, linting & testing

Pre defined scripts have been made to standardize the formatting, linting and testing. Before commiting your changes make sure you run and fix all issues for formatting, linting & testing.

We currenlty required a testing coverage of 95%

To run the formatting, linting and testing execute the following scripts:

```shell
./scripts/format
./script/lint
./script/test
```

We  currenlty require a high code coverage. So make sure you add tests when you create a client.

## Creating a new client

The steps to create a new client are faily simple.

1. copy the [dummy client](../blob/main/app/clients/dummy.py) in the app/clients/ folder.
2. change the [dummy client](../blob/main/app/clients/factory.py) to include the client with a special client_id
3. configure the application to use the client_id by setting the config CLIENT_IDS

after you the client does what you want add a test in tests/clients/ and write some documentation for the client in /docs/. After you are done create a PR in the github repository. Now just wait for it to be approved :D.
