#!/usr/bin/env python
from monitor import main, get_sites, ping, error_log, colorize
import pytest
import sys


def test_get_sites():
    """get_sites() function adds URLs from sys.argv"""
    sys.argv.append("www.google.com")
    sites = get_sites()
    assert "http://www.google.com" in sites


def test_colorize():
    """colorize() returns string wrapped in ANSI color tags"""
    assert colorize("text", "red") == "\033[91mtext\033[0m"
