# -*- coding: utf-8 -*-

tg_key = "XYZ"  # telegram bot api key

zbx_tg_prefix = "zbxtg"  # variable for separating text from script info
zbx_tg_tmp_dir = "/var/tmp/" + zbx_tg_prefix  # directory for saving caches, uids, cookies, etc.
zbx_tg_signature = False

zbx_tg_update_messages = True
zbx_tg_matches = {
    "problem": "PROBLEM: ",
    "ok": "OK: "
}

zbx_server = "http://127.0.0.1/zabbix/"  # zabbix server full url
zbx_api_user = "tg_graph"
zbx_api_pass = "zabbix.tg"

zbx_version = 6

zbx_basic_auth_user = "tg_graph"
zbx_basic_auth_pass = "zabbix.tg"

proxy_to_tg = None

zbx_db_host = "localhost"
zbx_db_database = "zabbix"
zbx_db_user = "tg_graph"
zbx_db_password = "zabbix.tg"


emoji_map = {
    "Disaster": "🔥",
    "High": "🛑",
    "Average": "❗",
    "Warning": "⚠️",
    "Information": "ℹ️",
    "Not classified": "🔘",
    "OK": "✅",
    "PROBLEM": "❗",
    "info": "ℹ️",
    "WARNING": "⚠️",
    "DISASTER": "❌",
    "bomb": "💣",
    "fire": "🔥",
    "hankey": "💩",
}
