#!/bin/sh

sudo killall axhttpd

python start_server.py \
		-p 80 \
		-s 443 \
		-c $1 \
		--nb_servers $2
