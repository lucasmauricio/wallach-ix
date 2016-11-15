#!/bin/ash

echo ""
echo "-----------------------------------------------------------"
echo ""
echo "Starting 'collection' service on (internal) port 8000"
echo "         ... but it will be binded to external port 7575"
echo ""

ping -c 2 www.google.com

ping -c 3 registrator

python /app-src/collection-service.py -p 8000
