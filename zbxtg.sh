#!/bin/bash
# Wrapper для отправки уведомлений в Telegram
# Использует Python из /opt/zbxtg/.venv

SCRIPT_DIR="/opt/zbxtg"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
ZBX_SCRIPT="$SCRIPT_DIR/zbxtg.py"

# Логирование ошибок (опционально)
LOG_FILE="/var/log/zabbix/zbxtg.log"

# Проверка существования Python в venv
if [ ! -f "$VENV_PYTHON" ]; then
    echo "$(date): ERROR - Python not found at $VENV_PYTHON" >> "$LOG_FILE"
    exit 1
fi

# Проверка существования скрипта
if [ ! -f "$ZBX_SCRIPT" ]; then
    echo "$(date): ERROR - Script not found at $ZBX_SCRIPT" >> "$LOG_FILE"
    exit 1
fi

# Запуск скрипта с передачей всех аргументов
exec "$VENV_PYTHON" "$ZBX_SCRIPT" "$@"