#!/data/data/com.termux/files/usr/bin/bash

# Ruta base del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_DIR="$PROJECT_DIR/db"
DB_FILE="$DB_DIR/productos.db"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

# Colores
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para mostrar mensajes de error
error_exit() {
  echo -e "${RED}[ERROR] $1${NC}" >&2
  exit 1
}

# Instalar dependencias
install_packages() {
  echo -e "${YELLOW}[+] Actualizando paquetes...${NC}"
  pkg update -y || error_exit "Falló al actualizar paquetes."

  echo -e "${YELLOW}[+] Instalando Python, SQLite y Git...${NC}"
  pkg install -y python sqlite git || error_exit "Falló al instalar dependencias."
}

# Configurar base de datos
setup_database() {
  echo -e "${YELLOW}[+] Verificando carpeta de la base de datos...${NC}"
  mkdir -p "$DB_DIR" || error_exit "No se pudo crear la carpeta 'db'."

  echo -e "${YELLOW}[+] Creando base de datos...${NC}"
  if sqlite3 "$DB_FILE" "CREATE TABLE IF NOT EXISTS productos (
        codigo TEXT PRIMARY KEY,
        fecha TEXT CHECK(fecha LIKE '____-__-__'),
        cantidad INTEGER,
        precio REAL
    );"; then
    echo -e "${GREEN}[✔] Base de datos creada en: $DB_FILE${NC}"
  else
    error_exit "Falló al crear la base de datos."
  fi
}

# Verificar instalación
check_install() {
  echo -e "\n${YELLOW}[+] Verificando instalación...${NC}"
  python --version || error_exit "Python no está instalado."
  sqlite3 --version || error_exit "SQLite no está instalado."

  if [ -f "$DB_FILE" ]; then
    echo -e "${GREEN}[✔] Base de datos encontrada: $DB_FILE${NC}"
  else
    error_exit "La base de datos no existe."
  fi
}

# Menú principal
main() {
  echo -e "\n${GREEN}=== Configuración del Proyecto en Termux ===${NC}"
  install_packages
  setup_database
  check_install

  echo -e "\n${GREEN}¡Configuración completada! 🎉${NC}"
  echo -e "Ejecuta: ${RED}cd $PROJECT_DIR && python scripts/manager.py${NC}"
}

main
