FROM postgres:15-alpine
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_HOST_AUTH_METHOD=trust
COPY $PWD/init.sql /docker-entrypoint-initdb.d/init.sql