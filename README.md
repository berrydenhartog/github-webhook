# Github webhook middleware

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/berrydenhartog/github-webhook/cicd.yml?label=tests)
![GitHub Release](https://img.shields.io/github/v/release/berrydenhartog/github-webhook?include_prereleases&sort=semver)
![GitHub License](https://img.shields.io/github/license/berrydenhartog/github-webhook)

The Github Webhook middleware allows you to convert and send [github event webhooks](https://docs.github.com/en/webhooks/webhook-events-and-payloads)  to another system like a postgresql, file, mongodb, mattermost, slack etc.

## How to use github webhook middleware

To use this application you need to deploy this application and configure github. The application is already packaged for you and available on [dockerhub](https://hub.docker.com/repository/docker/berrydenhartog/github-webhook) as a container.


### Configuring Application

This application uses environmental variables and/or yaml files to configure how the application behaves.

See [options](/docs/options.md) for all general options. For detailed options for every client see the [clients](#clients) documentation

### deploy application

Since the application is packaged as a container you can use allot of methods to deploy the application. We will explain 2.

1. running locally with docker compose
2. running in kubernetes with kustomize

#### docker compose

To run locally you can use the example [compose.yaml](compose.yaml)

```shell
docker compose build
docker compose up
```

This will rebuild the application an run it.

If you make some small edits to the compose.yaml you can skip the build step. change the folloing:

1. remove `build: .`
2. change `image: berrydenhartog/github-webhook:dev` to `image: berrydenhartog/github-webhook:latest`

By default the application is available on http://localhost:8000

#### kustomize

For an example of a kubernetes customize deployment see the [infra/](/infra/) folder.

you can deploy the application by running:

```shell
kubectl apply -k infra/overlays/production
```

You will propably need to make a few changes to the files to make it work for you.

### Configuring github

After you have deployed this application you need to configure the github webhook. This can be done one repository level or organisational level.

#### Organizational level

1. go to your organization (make sure you are an organizational admin)
2. go to `Settings`
3. go to `Webhooks`
4. click `Add webhook`
5. configure:
    - 'Payload URL': to the url you deployed the application
    - 'Content type': to `Application/json`
    - 'secret': to a random secret (make sure its the same as the variable GITHUB_WEBHOOK_SECRET)
    - select which events you want to receive.
6. Click `Add webhook` button
7. verify correct configuration by checking `Recent Deliveries ` under the webhook config

#### repository level

1. go to your repository (make sure you are an admin)
2. go to `Settings`
3. go to `Webhooks`
4. click `Add webhook`
5. configure:
    - 'Payload URL': to the url you deployed the application
    - 'Content type': to `Application/json`
    - 'secret': to a random secret (make sure its the same as the variable GITHUB_WEBHOOK_SECRET)
    - select which events you want to receive.
6. Click `Add webhook` button
7. verify correct configuration by checking `Recent Deliveries ` under the webhook config

## Clients

You can develop your own client or use one of the exising clients.

- [mattermost](./docs/mattermost-client.md): sends the event to a mattermost webhook
- [dummy](./docs/dummy-client.md): Does nothing with the event. DEFAULT

If you would like to add another client see the [How to Contribute](#How to Contribute)

## How to Contribute

See [Contributing](CONTRIBUTING.md)

## For developers

See [Contributing](/docs/developers.md)
