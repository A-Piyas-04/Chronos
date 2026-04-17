"""Shared Pydantic configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class OrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
