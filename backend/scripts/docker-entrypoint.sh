#!/usr/bin/env bash
set -e

# Run the init_db script if you want to create tables / seed
echo "Running init_db.py ..."
python scripts/init_db.py || true  # `|| true` to avoid failing container if the table already exists

# Then jump to the main container command
exec "$@"
