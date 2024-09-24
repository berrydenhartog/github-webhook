# Github Webhook options

The application can be configured using either environmental variables or a config.yaml file at the root of the application.

## Options

| Option  | Description   | Default  |
|---|---|---|
| LOGGING_LEVEL  | Default logging level  | INFO  |
| DEBUG  | debugging mode   |  False  |
| EXPORTER_IDS  | List of exporters to enable  | dummy  |
| WEBHOOK_SECRET  | secret to use when verifying request   | None |
| EVENT_FORMATS  | dictionary describing how to format a dict to a message  | {}  |
| EVENT_HEADER  | the header to extract the type of event  | x-github-event |
| EVENT_FILTERS  | dictionary describing the filter to apply on the json data | {}  |
| EVENT_TYPE_FILTERS  | dictionary describing the filter to apply on the event type from EVENT_HEADER | {}  |

## Exporter IDs

The application supports pluggable exporters. To find a exporter check the [exporters](../README.md#exporters
)

## Secret

The webhook secret can be enabled or disabled, but it is strongly recommended to enable it. Disabling the webhook secret leaves your endpoint exposed, allowing anyone to send requests to it.

To verify a message to the endpoint we use the github hashing system. Check the [github docs](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#python-example) on how the validation works.

## Filtering event type

We've implemented an filtering system that allows you to filter based on the event type. The event type is extracted from a header. The header is set by the option EVENT_HEADER.

There are ALLOW and DENY filters. You can specify either an ALLOW or DENY filter. A combination of the two is not recommended and the DENY will be ignored. If you only specify ALLOW we assume that you want to deny all other event-types.

An example filter of an ALLOW only. This will deny all other events that do not adhere to the default

```json
{
    "ALLOW": [
        "projects_v2",
        "projects_v2_item"
    ]
}
```

An example filter of an DENY only. This will deny only these events and allow all others.

```json
{
    "DENY": [
        "projects_v2",
        "projects_v2_item"
    ]
}
```

## Filtering event data

We've implemented an advanced filtering system that allows you to filter based on the entire JSON payload. This is achieved using [jq filters](https://jqlang.github.io/jq/manual/#basic-filters) combined with regular expression (Perl style) matching for precise control. to set a filter you need to configure the EVENT_FILTERS field.

A filter expression consists of a few parts:

1. ALLOW or DENY operator
2. JQ filter string
3. Compare Value or Regex statement


To explain how it works we use the following input json and describe some examples.

```json
{
    "sender": {"login": 123},
    "ref_type": "test",
    "ref": "test1",
    "repository": {"full_name": "123123"}
}
```

ALLOW filters allow you can always forward the message to a exporter. Is has precedeence over a deny filter. The bellow examples would both allow the example json to pass. The first is a normal compare and the second uses regex.

```json
{
    "ALLOW": [
        {"FILTER": ".sender.login", "VALUE": 123},
        {"FILTER": ".ref_type", "VALUE": "te.*"}
    ],
}
```

DENY filter are processed after the ALLOW filter and allow you to remove the message.
```json
{
    "DENY": [
        {"FILTER": ".ref", "VALUE": "test1"},
        {"FILTER": ".repository.fullname", "VALUE": "te.*"}],
}
```

If a jq filter matches more objects in a json it will pick the first one.

## Formatting

formatting allows you to convert a json object to a single message. For this you use python format strings. if no format string is found the application defaults to a string of the json.

By default the application uses formatting for most github events. See the defaults [here](../app/constants.py)

If you desire to change them you can set the EVENT_FORMATS.

A Format consists of 2 stings

1. the even type
2. the format string

To explain how it works we use the following input json and describe some examples.

```json
{
    "sender": {"login": 123},
    "ref_type": "test",
    "ref": "test1",
    "repository": {"full_name": "awesomerepo"}
}
```

lets assume the event-type from the EVENT_HEADER fields is `create` and we want to change the default formatting.

```json
{
    "commit_comment": "{comment[user][login]} commented on {comment[commit_id]} in {repository[full_name]}",
    "create": "{sender[login]} made branch {ref_type} ({ref}) in my {repository[full_name]}",
}
```

The first line is ignored because it is not the correct event-type. The second line will be applied and result in the following line:

    123 made branch test (test1) in my awesomerepo
