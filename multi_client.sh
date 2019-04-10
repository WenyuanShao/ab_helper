#!/bin/sh

sudo killall ab

if [ ! -d "logs" ]; then
	mkdir logs
fi

python start_clients.py \
		-p 443 \
		-k \
		--nb_cores $1 \
		--nb_request 10000 \
		--nb_client $2
