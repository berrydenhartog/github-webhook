# Developers

This application is developer in python 3 with fastapi. It uses a webhook endpoint at / that received all github webhook events.

The webhook events are processed and converted to a message. See [constatn.py](/app/contants.py) for the default conversion. after converting the github webhook event to a message the message is send to one of the clients for further handling. Depending on the client the message can be processed differenlty.

## Starting the application

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

We recommend using the pre-commit feature to have a standardized setup. Precommit does not check all things the CI/CD does but it does some.

to enable pre-commit do the following:

```shell
pre-comit install
```

Now, every time you do a git commit the pre-commit hooks will do validation of your files. Note: it does not run pyright.

## formatting, linting & testing

Pre defined scripts have been made to standardize the formatting, linting and testing. Before commiting your changes make sure you run and fix all issues for formatting, linting & testing.

We currenlty required a testing coverage of 95%

To run the formatting, linting and testing execute the following scripts:

```shell
./scripts/format
./script/lint
./script/test
```
