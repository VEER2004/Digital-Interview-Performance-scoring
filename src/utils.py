from __future__ import annotations
import pandas as pd

def make_display_name(col: str) -> str:
    return col.replace("_", " ")

def numeric_to_option(value, low, high):
    return int(value) if isinstance(value, float) and value.is_integer() else value