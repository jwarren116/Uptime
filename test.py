#!/usr/bin/env python
from monitor import main, get_sites, ping, error_log, colorize, last_email_time
import pytest
import sys
import io


def test_get_sites():
    """get_sites() function adds URLs from sys.argv"""
    sys.argv.append("www.google.com")
    assert "http://www.google.com" in get_sites()


def test_colorize():
    """colorize() returns string wrapped in ANSI color tags"""
    assert colorize("text", "red") == "\033[91mtext\033[0m"


def test_error_log(capsys):
    last_email_time["http://www.example.com"] = 0
    error_log("http://www.example.com", 404)
    log = [site.strip() for site in io.open('monitor.log', mode='r').readlines()]
    out, err = capsys.readouterr()
    assert "http://www.example.com STATUS: \033[93m404" in out
    assert "http://www.example.com STATUS: 404" in " ".join(log)


def test_ping_valid(capsys):
    ping("http://www.google.com")
    out, err = capsys.readouterr()
    assert "\033[92m." in out


def test_ping_invalid(capsys):
    last_email_time["http://www.jwarren.co/somefakesite"] = 0
    ping("http://www.jwarren.co/somefakesite")
    log = [site.strip() for site in io.open('monitor.log', mode='r').readlines()]
    out, err = capsys.readouterr()
    assert "http://www.jwarren.co/somefakesite STATUS: \033[93m404" in out
    assert "http://www.jwarren.co/somefakesite STATUS: 404" in " ".join(log)
