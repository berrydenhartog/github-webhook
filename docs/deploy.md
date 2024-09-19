# Deploy

Since the application is packaged as a container you can use all container deployment platforms or run it locally. We will explain 2 options.

1. running locally with docker compose
2. running in kubernetes with kustomize

## Run locally

To run locally you can use the example [compose.yaml](../compose.yaml)

```shell
docker compose build
docker compose up
```

This will rebuild the application an run it.

If you make some small edits to the compose.yaml you can skip the build step. change the folloing:

1. remove `build: .`
2. change `image: berrydenhartog/github-webhook:dev` to `image: berrydenhartog/github-webhook:latest`

By default the application is available on [localhost](http://localhost:8000)

## kustomize

For an example of a kubernetes kustomize deployment see the [infra/](/infra/) folder.

you can deploy the application by running:

```shell
kubectl apply -k infra/overlays/production
```

You will need to make a few changes to the files to make it work for you.
