# Fragment Stars API

<p align="center">
  <img src="https://img.shields.io/pypi/v/fragment-stars-api?color=blue" alt="PyPI version">
  <img src="https://img.shields.io/pypi/pyversions/fragment-stars-api" alt="Python versions">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**Python SDK для покупки Telegram Stars и Premium через Fragment.com**

Покупайте Telegram Stars и Premium подписки программно через блокчейн TON. Простой API, автоматическая подпись транзакций, очередь для Stars.

[🇬🇧 English version](README.md)

- Сайт с документацией: https://wemakecode.ru/fragment-api
- Production API endpoint: `https://fragment-api.ydns.eu:8443`
- Пример Telegram магазина: https://github.com/bbbuilt/tg_stars_premium_shop
- Промпты/skills для AI интеграции: [Codex](CODEX_SKILL.md) / [Claude](CLAUDE_SKILL.md) / [llms.txt](https://wemakecode.ru/fragment-api/llms.txt) / [llms-full.txt](https://wemakecode.ru/fragment-api/llms-full.txt)

## Vibe coding / настройка AI агента

Если клиент интегрирует API через Codex, Claude, Cursor или другой AI coding agent, сначала дайте агенту готовый skill-файл. Это защищает от типичных ошибок: придуманных API токенов, seed в frontend коде, утечек cookies и повторной покупки из-за слепого retry.

### Codex

1. Добавьте [CODEX_SKILL.md](CODEX_SKILL.md) в проект клиента.
2. Если в проекте есть `AGENTS.md`, добавьте:

```md
@CODEX_SKILL.md
```

3. Попросите Codex: `Интегрируй Fragment Stars API по project skill.`

### Claude

1. Добавьте [CLAUDE_SKILL.md](CLAUDE_SKILL.md) в проект клиента.
2. Скопируйте содержимое в `CLAUDE.md` или попросите Claude сначала прочитать `CLAUDE_SKILL.md`.
3. Попросите Claude: `Интегрируй Fragment Stars API по CLAUDE_SKILL.md.`

Важные правила для AI агентов:

- Клиентские вызовы API не требуют выданных API токенов или `X-API-Key`.
- Seed кошелька и Fragment cookies должны оставаться только на backend.
- KYC режим бесплатный навсегда: `0%` комиссии API.
- Нельзя делать слепой retry после того, как транзакция могла быть подписана или отправлена.

## Возможности

- ⭐ **Покупка Telegram Stars** — дарите звёзды любому пользователю Telegram
- 💎 **Покупка Telegram Premium** — подписки на 3, 6 или 12 месяцев
- 🔐 **KYC бесплатный навсегда** — в KYC режиме 0% комиссии API; если хотите перепроверить ставки перед использованием, вызовите `get_rates()`
- 🧩 **Два режима** — KYC со своими Fragment cookies или Non-KYC без cookies пользователя
- ⚡ **Автоматические транзакции** — просто укажите seed фразу, SDK сделает остальное
- 📊 **Управление очередью** — покупки Stars добавляются в очередь и автоматически опрашиваются
- 🛡️ **Type hints** — полная поддержка типов для автодополнения в IDE

## Установка

```bash
pip install fragment-stars-api
```

## Быстрый старт

```python
from fragment_api import FragmentAPIClient

# Инициализация с вашим API сервером
client = FragmentAPIClient("https://your-api-server.com:8443")

# Купить 50 звёзд для пользователя
result = client.buy_stars("username", 50, seed="your_seed_base64")

if result.success:
    print(f"✅ Отправлено {result.amount} звёзд!")
    print(f"💰 Стоимость: {result.cost_ton} TON")
else:
    print(f"❌ Ошибка: {result.error}")
```

## Примеры использования

### Покупка Stars (без KYC)

Использует аккаунт Fragment владельца API. Выше комиссия, но не нужны cookies пользователя.

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient("https://your-api-server.com:8443")

result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64"
)

print(f"Успех: {result.success}")
print(f"ID транзакции: {result.transaction_id}")
```

### Покупка Stars (с KYC)

Использует cookies пользователя Fragment. В KYC режиме **0% комиссии API навсегда**.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="wallet_seed_base64",
    cookies="user_fragment_cookies_base64"
)
```

### Покупка Premium

Покупки Premium обрабатываются API сразу и возвращают финальный результат напрямую.

```python
# 3 месяца
result = client.buy_premium("username", 3, seed="...")

# 6 месяцев
result = client.buy_premium("username", 6, seed="...")

# 12 месяцев
result = client.buy_premium("username", 12, seed="...")
```

### Проверка комиссий

KYC режим бесплатный навсегда, но перед использованием можно вызвать API и проверить текущие ставки.

```python
rates = client.get_rates()

print(f"Без KYC: {rates.rate_no_kyc}%")
print(f"С KYC: {rates.rate_with_kyc}%")
```

### Проверка статуса очереди

```python
status = client.get_queue_status()

print(f"Длина очереди: {status['queue_length']}")
print(f"Ожидание примерно: {status['estimated_wait_seconds']}s")
```

### Проверка доступности Premium

```python
result = client.check_premium_eligibility("username")

if result['eligible']:
    print("✅ Пользователь может купить Premium")
else:
    print(f"❌ Недоступно: {result.get('reason', 'Причина неизвестна')}")
```

### Асинхронный режим (не ждать)

```python
# Возвращает сразу с request_id
response = client.buy_stars("user", 50, seed="...", wait=False)
print(f"ID запроса: {response.request_id}")
print(f"Позиция в очереди: {response.position}")

# Проверить статус позже
status = client.get_status(response.request_id)
print(f"Статус: {status.status}")
```

## API Reference

### FragmentAPIClient

```python
FragmentAPIClient(
    base_url: str,              # Обязательный - URL вашего API сервера
    timeout: float = 30.0,
    poll_timeout: float = 300.0
)
```

### Методы

| Метод | Описание |
|-------|----------|
| `buy_stars(username, amount, seed, cookies?, local_storage?, wait?)` | Купить Telegram Stars через очередь |
| `buy_premium(username, duration, seed, cookies?, local_storage?, wait?)` | Купить Telegram Premium напрямую |
| `get_rates()` | Получить комиссии |
| `get_queue_status()` | Получить статус очереди и статистику |
| `check_premium_eligibility(username)` | Проверить доступность Premium для пользователя |
| `get_status(request_id)` | Получить статус запроса |

### Исключения

```python
from fragment_api import FragmentAPIError, QueueTimeoutError

try:
    result = client.buy_stars("user", 50, seed="...")
except QueueTimeoutError:
    print("Таймаут запроса")
except FragmentAPIError as e:
    print(f"Ошибка [{e.error_code}]: {e.message}")
```

## Как это работает

1. **Для Stars** вы вызываете `buy_stars()`, и API добавляет запрос в очередь
2. **SDK опрашивает** `GET /api/v1/queue/:request_id`, пока покупка Stars не завершится или не упадёт с ошибкой
3. **Для Premium** вы вызываете `buy_premium()`, и API возвращает финальный результат напрямую
4. **Сервер открывает** Fragment.com в headless браузере
5. **Сервер подписывает** TON транзакцию вашей seed фразой
6. **Stars/Premium доставляются** получателю в Telegram

## Требования

- Python 3.9+
- TON кошелёк с достаточным балансом
- Seed фраза кошелька (24 слова, base64)

### Как закодировать seed фразу

```bash
echo -n "word1 word2 word3 ... word24" | base64
```

### Как получить Fragment cookies (для KYC режима)

KYC режим требует ваши cookies от Fragment.com и имеет **0% комиссии API навсегда**.

> 📖 **[См. подробное руководство по кукам](https://github.com/bbbuilt/fragment-stars-api/blob/main/COOKIES_GUIDE.ru.md)** с пошаговыми инструкциями и решением проблем.

#### Краткое руководство

**Необходимые куки:**
- `stel_token` - Токен аутентификации сессии
- `stel_ssid` - ID сессии
- `stel_ton_token` - Токен подключения TON кошелька (**КРИТИЧНО - обязателен для покупок**)
- `stel_dt` - Смещение часового пояса

**Шаги:**

1. **Войдите на Fragment**: Перейдите на https://fragment.com и войдите через Telegram
2. **Подключите TON кошелёк**: Нажмите "Connect Wallet" и подключите Tonkeeper/MyTonWallet
3. **Откройте DevTools**: Нажмите F12 → Application → Cookies → https://fragment.com
4. **Скопируйте значения куков**: Скопируйте поле Value для каждой необходимой куки
5. **Создайте JSON**:
   ```json
   {
       "stel_token": "ваше_значение",
       "stel_ssid": "ваше_значение",
       "stel_ton_token": "ваше_значение",
       "stel_dt": "-180"
   }
   ```
6. **Закодируйте в base64**:
   ```bash
   cat cookies.json | base64 -w 0
   ```
7. **Используйте в коде**:
   ```python
   result = client.buy_stars(
       username="user",
       amount=50,
       seed="your_seed_base64",
       cookies="your_cookies_base64"
   )
   ```

> ⚠️ **Важно**: Кука `stel_ton_token` **обязательна** для покупок. Убедитесь, что ваш TON кошелёк подключён на fragment.com перед извлечением куков!

> 💡 **Совет**: KYC режим бесплатный навсегда, если вы передаёте Fragment cookies. Если не хотите возиться с куками, используйте No-KYC режим (просто не указывайте параметр `cookies`); у него есть комиссия, но куки не нужны.

## Автор

**Basebay** — Backend-разработчик, специализирующийся на автоматизации, ботах и инфраструктурных инструментах.

- Telegram: [@makecodev](https://t.me/makecodev)
- GitHub: [bbbuilt](https://github.com/bbbuilt)

## Поддержка

- GitHub Issues: [fragment-stars-api/issues](https://github.com/bbbuilt/fragment-stars-api/issues)
- Telegram: [@makecodev](https://t.me/makecodev)

## Лицензия

MIT License - см. файл [LICENSE](LICENSE).
