#!/bin/bash
export ANSIBLE_HOST_KEY_CHECKING=False
. ./unimelb-comp90024-2021-grp-25-openrc.sh; ansible-playbook mrc.yaml

ansible-playbook install_environments.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook couchdb_configuration.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook couchdb_slave0.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook couchdb_slave1.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook couchdb_cluster_install.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook git-download.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

ansible-playbook database-set.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem

nohup ansible-playbook searching.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem >/dev/null 2>&1&

nohup ansible-playbook streaming.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem >/dev/null 2>&1&

nohup ansible-playbook backend.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem >/dev/null 2>&1&

ansible-playbook nginx.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem