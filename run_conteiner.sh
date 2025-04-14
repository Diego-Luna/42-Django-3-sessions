
# * Run the docker-compose file
docker compose up --build -d


# * run the docker container
docker exec -it docker-compose-down-sessions /bin/zsh


# ? Run the postgresql container
docker exec -it postgres-db-3-sessions /bin/sh 

# ? delete the volume
# docker-compose down -v

# ? run informacion de la base de datos
# psql -U user -d ex00
# \dt -> show tables
# \d table_name -> show columns of table 
# \c ex00 -> connect to database ex00

# ? run the migrations
# python3 manage.py makemigrations ex03
# python3 manage.py migrate 

# python3 manage.py flush

# ? add date in de database

# python3 manage.py loaddata ../ex09_initial_data.json

# ? Clean de database
# python3 manage.py shell
# * Para eliminar todos los datos
# from ex09.models import People, Planets
# People.objects.all().delete()
# Planets.objects.all().delete()
# * Para verificar
# People.objects.count()  # Debería devolver 0
# Planets.objects.count()  # Debería devolver 0