#!/bin/bash

echo "===================="
echo "Update ZwiftRunalzye"
echo "===================="

docker-compose down
git pull
docker-compose up -d --build