from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.infra.db.database import Base  # Make sure this is the right declarative base
from app.modules.cause.models import *
from app.modules.donation.models import *
from app.modules.institute.models import *

# If models are in separate modules and use the same declarative base,
# importing them here ensures they're known to the MetaData
from app.modules.user.models import *

# Alembic Config object, which provides access to the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The MetaData object for 'autogenerate' support. This should be imported
# from the same place as your application's models use.
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Define the engine using the configuration from the .ini file.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Choose the running mode based on whether the script was called with the --sql flag.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
