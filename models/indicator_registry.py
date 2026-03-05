import os
import importlib
import re

INDICATORS = {}

INDICATOR_DIR = "indicators"

for filename in os.listdir(INDICATOR_DIR):

    # θέλουμε μόνο αρχεία τύπου i206.py
    if not filename.startswith("i") or not filename.endswith(".py"):
        continue

    module_name = filename[:-3]   # i206
    indicator_code = module_name[1:]  # 206

    module = importlib.import_module(f"{INDICATOR_DIR}.{module_name}")

    # default name
    name = f"Indicator {indicator_code}"

    # αν υπάρχει CONFIG μπορούμε να πάρουμε metadata
    config = getattr(module, "CONFIG", None)

    INDICATORS[indicator_code] = {
        "name": name,
        "module": module
    }

    if config:
        INDICATORS[indicator_code]["config"] = config

INDICATORS = dict(sorted(INDICATORS.items()))
