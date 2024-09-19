from typing import Any

from app.constants import FilterType, PermissionType
from app.eventhandlers import filter_event

FilterSuperType = dict[PermissionType, list[dict[FilterType, Any]]]


def test_eventhandler_filter_allow():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".sender.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allow_regex():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".ref_type", "VALUE": "te.*"}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allow_regex_nomatch():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".ref_type", "VALUE": "thahah*"}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allow_nomatch():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".hallo.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allow_incorrect_filter():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": "sender.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_deny():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "DENY": [{"FILTER": ".sender.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is True


def test_eventhandler_filter_deny_regex():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "DENY": [{"FILTER": ".ref_type", "VALUE": "te.*"}],
    }

    assert filter_event(filters, data) is True


def test_eventhandler_filter_deny_regex_nomatch():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "DENY": [{"FILTER": ".ref_type", "VALUE": "thahah*"}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_deny_nomatch():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "DENY": [{"FILTER": "sender.login", "VALUE": 456}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_deny_incorrect_filter():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "DENY": [{"FILTER": "sender.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allowdeny():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".sender.login", "VALUE": 123}],
        "DENY": [{"FILTER": ".sender.login", "VALUE": 123}],
    }

    assert filter_event(filters, data) is False


def test_eventhandler_filter_allowdeny_deny():
    data = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    filters: FilterSuperType = {
        "ALLOW": [{"FILTER": ".xxx.login", "VALUE": 123}],
        "DENY": [{"FILTER": ".ref", "VALUE": "test1"}],
    }

    assert filter_event(filters, data) is True
