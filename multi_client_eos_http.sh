#!/bin/sh

sudo killall lt-ab

if [ ! -d "logs" ]; then
	mkdir logs
fi
cd logs
rm -rf *
cd ..

python eos_start_clients_http.py \
		-p 443 \
		-k \
		--nb_cores $1 \
		--nb_request 1000 \
		--nb_client $2 \
		-R $3 \
