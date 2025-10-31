import os
import importlib

models_dir = os.path.dirname(__file__)

for file in os.listdir(models_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        # Import dynamically (e.g., app.models.linear_regression)
        importlib.import_module(f"{__name__}.{module_name}")

__all__ = [
    file[:-3]
    for file in os.listdir(models_dir)
    if file.endswith(".py") and file != "__init__.py"
]
