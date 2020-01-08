#!/usr/bin/env bash

docker cp ~/.pypirc manylinux:/home/
docker exec -i manylinux bash -c 'cd jmapper && twine upload --config-file /home/.pypirc wheelhouse/*'
