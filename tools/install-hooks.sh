#!/bin/sh
# Run once after cloning: sh tools/install-hooks.sh
cp tools/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "pre-commit hook installed: client-internal material will be blocked."
