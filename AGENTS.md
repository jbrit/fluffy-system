# Repository guidelines

Use Python 3.11+, Flask, SQLAlchemy and SQLite. Run `python -m pytest -q`.
The `/orders` body is a bare JSON array; keep its existing field names and types.
Keep the existing tests unchanged. This is a design gap in working code.
Add indexes only: do not change tables, columns, constraints or stored values.
Use integer cents for totals and UTC timestamps. The existing ID is SQLite
AUTOINCREMENT: insert through the normal allocator; never supply or reuse IDs.
Treat created_at, total and status as stable during a traversal; explain limits
for updates and deletes. No authentication, deployment or unrelated features.
Never invent measured performance or claim human/Gemini authorship without evidence.
