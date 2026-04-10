# Настройка отправки уведомлений Zabbix → Telegram с графиками

## 📋 Оглавление

1. [Предварительные требования](#предварительные-требования)
2. [Структура директорий](#структура-директорий)
3. [Установка Python и зависимостей](#установка-python-и-зависимостей)
4. [Настройка скрипта](#настройка-скрипта)
5. [Настройка Zabbix Server](#настройка-zabbix-server)
6. [Настройка Zabbix Web Interface](#настройка-zabbix-web-interface)
7. [Проверка и отладка](#проверка-и-отладка)
8. [Устранение неполадок](#устранение-неполадок)

---

## Предварительные требования

- Zabbix Server 6.4+ (работает и на более старых версиях)
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Доступ к серверу Zabbix с правами root
- Python 3.8+ (рекомендуется 3.14)

---

## Структура директорий

```txt
/opt/zbxtg/
├── .venv/                      # Виртуальное окружение Python
├── zbxtg.py                    # Основной скрипт
└── zbxtg_settings.py           # Конфигурация

/usr/lib64/zabbix/alertscripts/
└── zbxtg.sh                    # Wrapper-скрипт для Zabbix

/var/log/zabbix/
└── zbxtg.log                   # Лог-файл (опционально)
```

---

## Установка Python и зависимостей

```bash
mkdir -p /opt/zbxtg
```

Стянуть с репозитория файлы: `zbxtg.py` `zbxtg_settings.py` `requirements.txt`, затем сложить их в `/opt/zbxtg/`

```bash
export UV_PYTHON_INSTALL_DIR="/opt/python"
# Установка uv (менеджер Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.14.4

cd /opt/zbxtg
uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

## Настройка скрипта

### 1. Конфигурация `zbxtg_settings.py`

Откройте на редактирование файл `/opt/zbxtg/zbxtg_settings.py`:

```python

# ----------- Telegram -----------
tg_key = "YOUR_BOT_TOKEN"                    # Токен бота от @BotFather

# ----------- Zabbix -----------
zbx_server = "http://YOUR_ZABBIX_SERVER/zabbix"  # URL веб-интерфейса Zabbix
zbx_api_user = "YOUR_ZABBIX_USER"                # Пользователь (должен иметь права на графики)
zbx_api_pass = "YOUR_ZABBIX_PASSWORD"            # Пароль
zbx_server_version = 6                           # Версия Zabbix (6 для 6.4+)

# ----------- Настройки -----------
zbx_tg_prefix = "zbxtg;"                         # Префикс для параметров в сообщении
zbx_tg_tmp_dir = "/tmp/zbxtg"                    # Временная директория (измените!)
zbx_tg_signature = False                         # Подпись в конце сообщения

proxy_to_tg = "socks5://user:pass@ip:port"              # Прокси для Telegram
```

### 2. Создание wrapper-скрипта

см. `zbxtg.sh` в корне репозитория

Куда положить на сервер ?: `/usr/lib64/zabbix/alertscripts/zbxtg.sh`:

```bash
# Установка прав
chmod +x /usr/lib64/zabbix/alertscripts/zbxtg.sh
```

---

## Настройка Zabbix Server

### 1. Настройка прав на временную директорию

**Важно:** Измените `zbx_tg_tmp_dir` в `zbxtg_settings.py` на нестандартный путь (рекомендация автора скрипта):

```python
zbx_tg_tmp_dir = "/var/tmp/zbxtg"  # или /opt/zbxtg/tmp
```

```bash
mkdir -p /var/tmp/zbxtg
chmod 755 /var/tmp/zbxtg
```

### 2. Проверка скрипта

```bash
# Тестовый запуск
 /usr/lib64/zabbix/alertscripts/zbxtg.sh "group_name" "Test" "Test message"

# Должно прийти сообщение в Telegram
```

---

## Настройка Zabbix Web Interface

### 1. Создание Media Type

**Administration → Media types → Create media type**

см. `MediaTypeConfig.png`

| Поле | Значение |
|------|----------|
| Name | `Telegram via venv` |
| Type | `Script` |
| Script name | `zbxtg.sh` |

**Script parameters (3 параметра):**
| Параметр | Значение |
|----------|----------|
| Parameter 1 | `{ALERT.SENDTO}` |
| Parameter 2 | `{ALERT.SUBJECT}` |
| Parameter 3 | `{ALERT.MESSAGE}` |

### 2. Настройка пользователя

**Administration → Users** → выберите пользователя → вкладка **Media** → **Add**

| Поле | Значение |
|------|----------|
| Type | `Telegram via venv` |
| Send to | `group_name` |
| When active | `1-7,00:00-24:00` |
| Use if severity | `All` |

### 3. Настройка Action

**Configuration → Actions → Trigger actions** → **Create action**

**Вкладка Actions:**
- **Name:** `Telegram notifications`

**Вкладка Operations:**
- Нажмите **Add** → **Operation type:** `Send message`
- **Send to users:** выберите вашего пользователя

**Для сообщения о проблеме (Problem):**
см. /message_templates/Problem.md

**Вкладка Recovery operations:**
см. /message_templates/Recovery.md

Сохраните Action.

---

### Доступные параметры

| Параметр | Описание | Пример |
|----------|----------|--------|
| `zbxtg;graphs` | Включить отправку графика | `zbxtg;graphs` |
| `zbxtg;itemid:123` | ID элемента данных | `zbxtg;itemid:12345` |
| `zbxtg;title:My Graph` | Заголовок графика | `zbxtg;title=CPU Load` |
| `zbxtg;graphs_period=3600` | Период в секундах | `zbxtg;graphs_period=10800` |
| `zbxtg;graphs_age=1h` | Период в формате | `zbxtg;graphs_age=3h` |
| `zbxtg;graphs_width=900` | Ширина графика | `zbxtg;graphs_width=800` |
| `zbxtg;graphs_height=200` | Высота графика | `zbxtg;graphs_height=250` |
| `zbxtg;single_message` | Текст + график в одном | `zbxtg;single_message` |

---

## Проверка и отладка


### Тест из веб-интерфейса

1. **Administration → Media types** → `Telegram via venv`
2. Нажмите **Test**
3. Введите:
   - **Send to:** `group_name`
   - **Subject:** `Test Subject`
   - **Message:** `Test Message`
4. Нажмите **Test**

**Примечание:** Макросы (`{ALERT.SUBJECT}`) в тесте не заменяются — это нормально.

### Просмотр логов

```bash
# Лог Zabbix Server
tail -f /var/log/zabbix/zabbix_server.log

# Лог скрипта
tail -f /var/log/zabbix/zbxtg.log

# Включение отладки в скрипте
# Добавьте --debug в wrapper:
exec "$VENV_PYTHON" "$ZBX_SCRIPT" "$@" --debug 2>> "$LOG_FILE"
```

---

## Устранение неполадок

### 1. Permission denied при запуске

```bash
chmod +x /usr/lib64/zabbix/alertscripts/zbxtg.sh
```

### 2. Login to Zabbix web UI has failed

Проверьте в `zbxtg_settings.py`:

- `zbx_server` — полный URL до веб-интерфейса (например, `http://server/zabbix`)
- `zbx_api_user` / `zbx_api_pass` — пользователь от веб-интерфейса (НЕ API)
- Пользователь должен иметь права на просмотр графиков

### 3. File not found при curl

Исправьте путь в `zbx_server`. Проверьте реальный путь до Zabbix.

### 4. Модуль zbxtg_settings не найден

Поместите `zbxtg_settings.py` в ту же директорию, что и `zbxtg.py`:

```bash
cp /path/to/zbxtg_settings.py /opt/zbxtg/
```

### 5. Пользователь должен начать диалог с ботом

В личных сообщениях: пользователь должен сначала отправить любое сообщение боту.

В группах: бот должен быть добавлен в группу.


---

## Ссылки

- [Официальный репозиторий оригинального скрипта](https://github.com/ableev/Zabbix-in-Telegram)
- [Полная документация по параметрам](https://github.com/ableev/Zabbix-in-Telegram/wiki/Settings)

---