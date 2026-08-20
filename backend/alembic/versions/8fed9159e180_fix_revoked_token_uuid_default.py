from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8fed9159e180"
down_revision: Union[str, Sequence[str], None] = "592696235890"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE revoked_tokens
        ALTER COLUMN id
        SET DEFAULT gen_random_uuid();
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE revoked_tokens
        ALTER COLUMN id
        DROP DEFAULT;
    """)