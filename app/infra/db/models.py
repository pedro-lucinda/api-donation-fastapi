"""
This module consolidates the imports of models from different modules within
the application, allowing them to be imported from a single location. This
approach simplifies import statements elsewhere in the application and provides
a central place to manage model imports.

The `__all__` list explicitly declares the names that should be imported when
`from <module> import *` is used on this module. It helps to control the
namespace exposed by the module and prevent unintended imports.
"""

from app.modules.cause.models import Cause
from app.modules.donation.models import Donation
from app.modules.institute.models import Institute

# Import models from each module
from app.modules.user.models import User

# Expose them through a single interface
__all__ = [
    "User",
    "Donation",
    "Cause",
    "Institute",
]
