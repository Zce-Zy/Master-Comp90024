#!/bin/bash
export ANSIBLE_HOST_KEY_CHECKING=False
. ./unimelb-comp90024-2021-grp-25-openrc.sh; ansible-playbook backend.yaml -i inventory/hosts.ini -u ubuntu --key-file=/home/rex/Downloads/Group25.pem