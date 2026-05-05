"""LLM cmd plugin package.

This package provides the ``llm cmd`` top-level command and supporting
modules split by responsibility for incremental feature development.
"""

from llm import hookimpl

from .plugin import register_commands

__all__ = ["register_commands", "hookimpl"]
