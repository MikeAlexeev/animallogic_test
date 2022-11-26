#!/usr/bin/env bash

set -eu


echo installing dependencies
make venv > /dev/null
. .venv/bin/activate

echo installing user-manager package
make install-editable > /dev/null

set -x

echo -e "\n# add first user, personal info by default"
user-manager set user1 --address some-address --phone-number 1234

echo -e "\n# show user1 info"
user-manager get user1

echo -e "\n# add first user work info"
user-manager set user1 work --address some-address2 --phone-number 567

echo -e "\n# add another user, pass phone-number only"
user-manager set user2 --phone-number 12345

echo -e "\n# list all users"
user-manager get-all

echo -e "\n# update user2"
user-manager set user2 --phone-number new-phone --address city3

echo -e "\n# remove user1 personal info"
user-manager remove user1 personal

echo -e "\n# show user1 info"
user-manager get user1

echo -e "\n# remove user1 all info"
user-manager remove user1

echo -e "\n# use json plugin for output"
user-manager --plugins-dir ./plugin_example --output json get-all
