#!/bin/bash
set -e

if [ -z "$RABBITMQ_DEFAULT_USER" ] || [ -z "$RABBITMQ_DEFAULT_PASS" ]; then
    echo "ERROR: Required environment variables not set"
    exit 1
fi

# Генерируем хеш пароля и берём последнюю строку (сам хеш), удаляем возможные переводы строк
RABBITMQ_PASS_HASH=$(rabbitmqctl hash_password "$RABBITMQ_DEFAULT_PASS" | tail -n1 | tr -d '\n\r')
# echo "Hash generated: $RABBITMQ_PASS_HASH"

TARGET="/etc/rabbitmq/definitions.d/20-defs-users.json"

# Создаём JSON с помощью here-document
cat > "$TARGET" <<EOF
{
  "users": [
    {
      "name": "${RABBITMQ_DEFAULT_USER}",
      "password_hash": "${RABBITMQ_PASS_HASH}",
      "tags": "administrator"
    }
  ],
  "permissions": [
    {
      "user": "${RABBITMQ_DEFAULT_USER}",
      "vhost": "/",
      "configure": ".*",
      "write": ".*",
      "read": ".*"
    }
  ]
}
EOF

# Проверяем, что файл не содержит плейсхолдеров
if grep -q '\${' "$TARGET"; then
    echo "ERROR: Placeholders still present in file"
    exit 1
fi

echo "=== pass_hash.sh completed, starting RabbitMQ ==="
exec rabbitmq-server