#!/bin/bash
/home/beny/github/pyopenvpn-web/.venv/bin/python /home/beny/github/pyopenvpn-web/manage.py connect -n $common_name -i $trusted_ip -p $trusted_port

