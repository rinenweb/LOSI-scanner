from indicators import i206, i214, i234, i273, i204

INDICATORS = {
    "206": {"name": "Internal search mechanism", "module": i206},
    "214": {"name": "Contact details", "module": i214},
    "234": {"name": "Privacy policy", "module": i234, "config": i234.CONFIG},
    "273": {"name": "Social networking features", "module": i273},
    "204": {"name": "Mobile device accessibility", "module": i204},
}
