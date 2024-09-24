# Mattermost exporter

The Mattermost Exporter sends messages to a mattermost [incoming webhook](https://developers.mattermost.com/integrate/webhooks/incoming/). Mattermost is a chat application.

The exporter has the exporter_id: 'mattermost'

Options can be configured as environmental variable os in a mattermost.yaml config file. If the file is used you can ommit the MATERMOST_ from the options.

## Options

| Option  | Description   | Default  |
|---|---|---|
| MATTERMOST_DEFAULT_CHANNEL | channel to send message too | None  |
| MATTERMOST_EVENT_CHANNEL_MAPPING  | map event-type to channel |  {}  |
| MATTERMOST_URL | URL of the webhook | [required] |

## Default channel

If the MATTERMOST_DEFAULT_CHANNEL is not set the incomming webhook will send the message to the incomming webhook default channel. this is configured on creating the incomming webhook in mattermost.

## EVENT_CHANNEL_MAPPING

The event channel mapping is able to change the delivery of a message to a channel based on the event-type. This is only possible if the mattermost incomming webhook allows this.

an example of how this would look:

```json
{
  "create": "channel1",
  "delete": "channel2"
}
```
