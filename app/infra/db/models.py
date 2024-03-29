# infra/db/models.py

# Import models from each module
from app.modules.user.models import User, Item
# Import other models as needed
# from app.modules.othermodule.models import OtherModel

# Expose them through a single interface
__all__ = [
    "User",
    "Item",
    # "OtherModel",  # Uncomment or add new models as they are created
]
