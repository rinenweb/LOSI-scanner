import os
import importlib

INDICATORS = {}

INDICATOR_DIR = "indicators"

for filename in os.listdir(INDICATOR_DIR):

    if not filename.startswith("i") or not filename.endswith(".py"):
        continue

    module_name = filename[:-3]   # i206
    indicator_code = module_name[1:]  # 206

    module = importlib.import_module(f"{INDICATOR_DIR}.{module_name}")

    # πάρε CONFIG αν υπάρχει
    config = getattr(module, "CONFIG", {})
    
    # όνομα indicator
    name = config.get("name", f"Indicator {indicator_code}")
    
    # description
    description = config.get("description")
    
    INDICATORS[indicator_code] = {
        "name": name,
        "description": description,
        "module": module
    }

    if config:
        INDICATORS[indicator_code]["config"] = config

INDICATORS = dict(sorted(INDICATORS.items()))
