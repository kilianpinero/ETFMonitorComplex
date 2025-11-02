# Usa la imagen oficial de PostgreSQL
FROM postgres:16

# Establece variables de entorno para la configuración inicial
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123
ENV POSTGRES_DB=ETF_monitor_local

# Copia archivos de inicialización si los tienes (opcional)
# COPY init.sql /docker-entrypoint-initdb.d/

# Expone el puerto por defecto de PostgreSQL
EXPOSE 5432