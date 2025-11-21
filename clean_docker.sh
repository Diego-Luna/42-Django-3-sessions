#!/bin/bash

echo "--- Starting Docker cleanup for the project ---"
echo " - Stopping containers, removing containers, networks, volumes, and the built image..."

# The 'down' command stops and removes containers and networks.
# --volumes: Removes the named volumes declared in the 'volumes' section of the Compose file.
# --rmi 'local': Removes images that were built locally for the services.
docker compose down --volumes --rmi 'local'

echo "--- Docker cleanup complete! ---"