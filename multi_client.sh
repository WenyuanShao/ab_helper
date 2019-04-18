#!/bin/sh

sudo killall lt-ab

if [ ! -d "logs" ]; then
	mkdir logs
fi
cd logs
rm -rf *
cd ..

python start_clients.py \
		-l \
		-k \
		-s 10.10.1.7\
                -R 1000 \
		--nb_cores $1 \
		--nb_request 10000 \
		--nb_client $2 \
		--increment 1 \
		--first_https_port 443 \
		--first_client_port 11211 \
