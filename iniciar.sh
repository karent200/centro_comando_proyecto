#!/bin/bash
# Arranca el servidor Django - Centro de Comando
# Ejecuta: bash iniciar.sh

PROYECTO="/home/karent/Documentos/Universidad/Desarrollo web/project1"
URL="http://127.0.0.1:8000/admin/"

cd "$PROYECTO" || { echo "[ERROR] No existe $PROYECTO"; exit 1; }

if [ ! -d ".venv" ]; then
    echo "[ERROR] Falta el entorno virtual."
    echo "Ejecuta: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

if [ ! -f "manage.py" ]; then
    echo "[ERROR] No se encontró manage.py en $PROYECTO"
    exit 1
fi

# Detener servidores viejos rotos
pkill -f "manage.py runserver" 2>/dev/null
sleep 1

echo "Iniciando Django..."
echo "NO CIERRES esta ventana mientras uses el admin."
echo ""

# Servidor en primer plano (así ves errores si hay)
exec .venv/bin/python manage.py runserver 127.0.0.1:8000
