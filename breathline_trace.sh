#!/bin/bash

LOGFILE="/var/log/jetson_breathline.jsonl"
PY_SCRIPT_PATH="$HOME/spiral-ambient/spiral-ambient-systems/read_bme680.py"

# Ensure the log directory exists
mkdir -p "$(dirname "$LOGFILE")"

# Timestamp
TIMESTAMP=$(date -Iseconds)

# CPU Temp
RAW_TEMP=$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null)
if [[ "$RAW_TEMP" =~ ^[0-9]+$ ]]; then
  CPU_TEMP=$(awk "BEGIN {print $RAW_TEMP / 1000}")
else
  CPU_TEMP="null"
fi

# CPU Load
RAW_LOAD=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/")
if [[ "$RAW_LOAD" =~ ^[0-9.]+$ ]]; then
  CPU_LOAD=$(awk "BEGIN {print 100 - $RAW_LOAD}")
else
  CPU_LOAD="null"
fi

# Get ambient sensor JSON
BME680_JSON=$(python3 "$PY_SCRIPT_PATH" 2>/dev/null)

# Use jq to extract fields (allow null fallback)
get_or_null() {
  echo "$BME680_JSON" | jq -r "$1 // empty" 2>/dev/null || echo "null"
}

AMBIENT_TEMP=$(get_or_null '.ambient_temp')
HUMIDITY=$(get_or_null '.humidity')
PRESSURE=$(get_or_null '.pressure')
VOC_LEVEL=$(get_or_null '.voc_level')
LIGHT_LEVEL=$(get_or_null '.light_level')
SENSOR_ERROR=$(get_or_null '.sensor_error')

# Build JSON (safe handling of nulls/values)
JSON_OUTPUT=$(jq -n \
  --arg timestamp "$TIMESTAMP" \
  --argjson cpu_temp "${CPU_TEMP:-null}" \
  --argjson cpu_load "${CPU_LOAD:-null}" \
  --argjson ambient_temp "${AMBIENT_TEMP:-null}" \
  --argjson humidity "${HUMIDITY:-null}" \
  --argjson pressure "${PRESSURE:-null}" \
  --argjson voc_level "${VOC_LEVEL:-null}" \
  --argjson light_level "${LIGHT_LEVEL:-null}" \
  --arg sensor_error "$SENSOR_ERROR" \
  '{
    timestamp: $timestamp,
    cpu_temp: $cpu_temp,
    cpu_load: $cpu_load,
    ambient_temp: $ambient_temp,
    humidity: $humidity,
    pressure: $pressure,
    voc_level: $voc_level,
    light_level: $light_level,
    sensor_error: $sensor_error
  }'
)

# Append to the .jsonl file
echo "$JSON_OUTPUT" | sudo tee -a "$LOGFILE" > /dev/null

