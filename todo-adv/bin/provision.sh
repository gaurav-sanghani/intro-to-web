#!/usr/bin/env bash

echo "******************************************************"
echo "**                                                  **"
echo "**              PROVISIONING                        **"
echo "**                                                  **"
echo "******************************************************"
echo
date
echo

echo "Creating vagrant PG user..."

su - postgres -c "psql template1 -c \"create user vagrant superuser password 'vagrant'\""
su - vagrant -c "psql template1 -c \"create database vagrant\""

cd /vagrant && make build