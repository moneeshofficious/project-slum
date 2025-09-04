# app/data/migrations/env.py
from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# This Alembic Config object provides access to values within alembic.ini
config = context.config

# Set up logging using alembic.ini, but keep existing app loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Prefer env var; fallback to alembic.ini value
db_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
config.set_main_option("sqlalchemy.url", db_url)

# If you have a declarative Base, import and set it here for autogenerate:
# from app.data.models import Base
target_metadata = None  # replace with Base.metadata when ready

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
