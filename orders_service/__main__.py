import argparse
from pathlib import Path
from . import create_app
from .seed import seed


def main():
    parser = argparse.ArgumentParser(description="Local orders API demo")
    sub = parser.add_subparsers(dest="command", required=True)
    seed_parser = sub.add_parser("seed")
    seed_parser.add_argument("--rows", type=int, default=100_000)
    serve_parser = sub.add_parser("serve")
    serve_parser.add_argument("--port", type=int, default=5000)
    sub.add_parser("migrate")
    args = parser.parse_args()
    app = create_app()
    if args.command == "seed":
        if args.rows < 0:
            parser.error("rows must be non-negative")
        print(f"Seeded {seed(app.extensions['orders_engine'], args.rows):,} orders")
    elif args.command == "migrate":
        migration = Path(__file__).resolve().parents[1] / "migrations" / "001_order_pagination.sql"
        if not migration.exists():
            parser.error("No pagination migration in the starter; apply the solution first")
        with app.extensions["orders_engine"].begin() as conn:
            for statement in migration.read_text().split(";"):
                if statement.strip():
                    conn.exec_driver_sql(statement)
        print("Applied index migration (idempotent)")
    else:
        app.run(host="127.0.0.1", port=args.port, debug=False)


if __name__ == "__main__":
    main()
