"""Configuration file parsing."""

from configlib import loadcfg


__all__ = ['CONFIG']


CONFIG = loadcfg('tenantforum.conf')
