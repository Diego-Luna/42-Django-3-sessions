
#!/bin/bash

# Stop any previous containers if they exist
echo "Cleaning up previous containers..."
docker compose down 2>/dev/null

# Build and start containers
echo "Building and starting containers..."
docker compose up --build -d

echo "Waiting for services to be ready..."
sleep 5

# Check container status
echo ""
echo "Containers status:"
docker ps --filter "name=docker-compose-down-sessions" --filter "name=postgres-db-3-sessions"

echo ""
echo "Containers started!"
echo ""
echo "To run Django inside the container, run:"
echo "   cd sessions"
echo "   python3 manage.py migrate"
echo "   python3 manage.py runserver 0.0.0.0:8000"
echo ""
echo "Or use the helper script:"
echo "   cd sessions"
echo ""
echo "The server will be available at: http://localhost:8000"
echo ""
echo "Opening Django container shell..."
echo ""

# Open a shell in the Django container
docker exec -it docker-compose-down-sessions /bin/zsh

x