FROM debian:bullseye-slim

# Evitar interacciones durante la instalación de paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalar paquetes necesarios y herramientas adicionales
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    zsh \
    git \
    curl \
    wget \
    vim \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Configurar zsh como shell por defecto
RUN chsh -s /usr/bin/zsh root

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Comando por defecto al iniciar el contenedor
CMD ["tail", "-f", "/dev/null"]