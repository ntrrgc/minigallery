FROM docker.io/library/httpd:2.4-bookworm
RUN apt-get update
RUN apt-get install -y vim iproute2 less iptables

RUN sed -i \
                -e 's/^#\(Include .*httpd-ssl.conf\)/\1/' \
                -e 's/^#\(LoadModule .*mod_ssl.so\)/\1/' \
                -e 's/^#\(LoadModule .*mod_socache_shmcb.so\)/\1/' \
                -e 's/^#\(LoadModule .*mod_http2.so\)/\1/' \
                conf/httpd.conf
RUN echo 'Protocols h2 http/1.1' >> conf/httpd.conf
COPY cert.pem /usr/local/apache2/conf/server.crt
COPY key.pem /usr/local/apache2/conf/server.key

ENV SSLKEYLOGFILE=/sslkey.log