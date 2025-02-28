from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "applications" (
    "is_active" BOOL NOT NULL DEFAULT True,
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "company_id" UUID NOT NULL REFERENCES "companies" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "applications";"""
