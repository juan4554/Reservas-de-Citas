"""add activo field to user

Revision ID: 3c27f74c6566
Revises: 53b695715c54
Create Date: 2025-12-13 19:39:11.826168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c27f74c6566'
down_revision: Union[str, Sequence[str], None] = '53b695715c54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite no soporta ALTER COLUMN, así que solo añadimos la columna activo
    # y establecemos un valor por defecto
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activo', sa.Boolean(), nullable=False, server_default='1'))
    
    # Asegurar que todos los usuarios existentes tengan activo=True
    op.execute("UPDATE usuarios SET activo = 1 WHERE activo IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('activo')
