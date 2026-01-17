# Fragment Stars API

<p align="center">
  <img src="https://img.shields.io/pypi/v/fragment-stars-api?color=blue" alt="PyPI version">
  <img src="https://img.shields.io/pypi/pyversions/fragment-stars-api" alt="Python versions">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**Python SDK для покупки Telegram Stars и Premium через Fragment.com**

Покупайте Telegram Stars и Premium подписки программно через блокчейн TON. Простой API, автоматическая подпись транзакций, управление очередью.

[🇬🇧 English version](README.md)

## Возможности

- ⭐ **Покупка Telegram Stars** — дарите звёзды любому пользователю Telegram
- 💎 **Покупка Telegram Premium** — подписки на 3, 6 или 12 месяцев
- 🔐 **Два режима** — с KYC и без (разные комиссии)
- ⚡ **Автоматические транзакции** — просто укажите seed фразу, SDK сделает остальное
- 📊 **Управление очередью** — автоматический polling результатов
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
print(f"Транзакция: {result.transaction_hash}")
```

### Покупка Stars (с KYC)

Использует cookies пользователя Fragment. Ниже комиссия.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="wallet_seed_base64",
    cookies="user_fragment_cookies_base64"
)
```

### Покупка Premium

```python
# 3 месяца
result = client.buy_premium("username", 3, seed="...")

# 6 месяцев
result = client.buy_premium("username", 6, seed="...")

# 12 месяцев
result = client.buy_premium("username", 12, seed="...")
```

### Проверка комиссий

```python
rates = client.get_rates()

print(f"Без KYC: {rates.rate_no_kyc}%")
print(f"С KYC: {rates.rate_with_kyc}%")
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
| `buy_stars(username, amount, seed, cookies?, wait?)` | Купить Telegram Stars |
| `buy_premium(username, duration, seed, cookies?, wait?)` | Купить Telegram Premium |
| `get_rates()` | Получить комиссии |
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

1. **Вы вызываете** `buy_stars()` или `buy_premium()`
2. **API создаёт** запрос на покупку и добавляет в очередь
3. **Сервер открывает** Fragment.com в headless браузере
4. **Сервер подписывает** TON транзакцию вашей seed фразой
5. **Транзакция отправляется** в блокчейн TON
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

KYC режим требует ваши cookies от Fragment.com. Вот как их получить:

#### Шаг 1: Войдите на Fragment

1. Откройте браузер Chrome
2. Перейдите на https://fragment.com
3. Нажмите "Log In" и авторизуйтесь через Telegram

#### Шаг 2: Откройте инструменты разработчика

1. Нажмите `F12` или `Ctrl+Shift+I` (Windows/Linux) или `Cmd+Option+I` (Mac)
2. Перейдите на вкладку **Application** (Приложение)
3. В левой панели разверните **Cookies**
4. Нажмите на `https://fragment.com`

#### Шаг 3: Скопируйте нужные cookies

Вам нужны эти 4 cookie:

| Имя Cookie | Описание |
|------------|----------|
| `stel_ton_token` | Токен авторизации TON кошелька |
| `stel_token` | Токен сессии |
| `stel_ssid` | ID сессии |
| `stel_dt` | Смещение часового пояса |

Для каждого cookie скопируйте поле **Value** (Значение).

#### Шаг 4: Создайте JSON файл

Создайте файл `cookies.json` в таком формате:

```json
{
    "stel_ton_token": "вставьте_значение_сюда",
    "stel_token": "вставьте_значение_сюда",
    "stel_ssid": "вставьте_значение_сюда",
    "stel_dt": "-180"
}
```

#### Шаг 5: Закодируйте в base64

**Linux/Mac:**
```bash
cat cookies.json | base64
```

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content cookies.json -Raw)))
```

**Python:**
```python
import base64
import json

cookies = {
    "stel_ton_token": "ваше_значение",
    "stel_token": "ваше_значение",
    "stel_ssid": "ваше_значение",
    "stel_dt": "-180"
}

encoded = base64.b64encode(json.dumps(cookies).encode()).decode()
print(encoded)
```

#### Шаг 6: Используйте в коде

```python
result = client.buy_stars(
    username="user",
    amount=50,
    seed="your_seed_base64",
    cookies="your_cookies_base64"  # Вставьте закодированную строку
)
```

> ⚠️ **Безопасность:** Никогда не делитесь своими cookies! Они дают полный доступ к вашему аккаунту Fragment.

## Автор

**Basebay** — Backend-разработчик, специализирующийся на автоматизации, ботах и инфраструктурных инструментах.

- Telegram: [@basebay](https://t.me/basebay)
- GitHub: [bbbuilt](https://github.com/bbbuilt)

## Поддержка

- GitHub Issues: [fragment-stars-api/issues](https://github.com/bbbuilt/fragment-stars-api/issues)
- Telegram: [@basebay](https://t.me/basebay)

## Лицензия

MIT License - см. файл [LICENSE](LICENSE).
