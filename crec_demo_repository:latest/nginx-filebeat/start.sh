#!/bin/bash
python /home/ian/crec_demo_compose/crec_docker:latest/generatedata.py
curl -XPUT -H "Content-Type: application/json" 'http://localhost:9200/_template/filebeat?pretty' -d@/etc/filebeat/filebeat.template.json
/etc/init.d/filebeat start.sh
cat /tmp/Equip_log_files/
