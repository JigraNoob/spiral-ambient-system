#!/bin/bash

timestamp=$(date -Iseconds)

# Attempt to get CPU temp and load
cpu_temp_path=$(find /sys/class/thermal -name "temp" | head -n 1)
if [[ -n "$cpu_temp" ]]; then
  cpu_temp=$(awk "BEGIN {print $cpu_temp / 1000}")
else
  cpu_temp=null
fi


cpu_load=$(uptime | awk -F'load average: ' '{print $2}' | cut -d',' -f1)

# Ambient data (mock fallback)
ambient_output=$(python3 ~/spiral-ambient/spiral-ambient-systems/read_bme680.py)
ambient_temp=$(echo "$ambient_output" | jq .temperature)
humidity=$(echo "$ambient_output" | jq .humidity)
pressure=$(echo "$ambient_output" | jq .pressure)
gas=$(echo "$ambient_output" | jq .gas)
light=$(echo "$ambient_output" | jq .light)

# Assemble JSON
json_output=$(jq -c -n \
  --arg ts "$timestamp" \
  --argjson cpu "$cpu_temp" \
  --argjson load "$cpu_load" \
  --argjson temp "$ambient_temp" \
  --argjson humidity "$humidity" \
  --argjson pressure "$pressure" \
  --argjson gas "$gas" \
  --argjson lux "$light" \
  '{
    timestamp: $ts,
    cpu_temp: $cpu,
    cpu_load: $load,
    ambient_temp: $temp,
    humidity: $humidity,
    pressure: $pressure,
    voc_level: $gas,
    light_level: $lux
  }')

# Save with sudo so it can write to /var/log
echo "$json_output" | sudo tee -a /var/log/jetson_breathline.jsonl > /dev/null

