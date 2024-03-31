"""
This module consolidates the imports of models from different modules within
the application, allowing them to be imported from a single location. This
approach simplifies import statements elsewhere in the application and provides
a central place to manage model imports.

The `__all__` list explicitly declares the names that should be imported when
`from <module> import *` is used on this module. It helps to control the
namespace exposed by the module and prevent unintended imports.
"""

# Import models from each module
from app.modules.user.models import Item, User

# Expose them through a single interface
__all__ = [
    "User",
    "Item",
]
