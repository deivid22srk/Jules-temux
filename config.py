import os

JULES_API_KEY = os.getenv('JULES_API_KEY', 'AQ.Ab8RN6LY7q3eWYwVUdQUWOCUJdzJO7EIvlCibJP3ZY-TO4-Xmg')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8223002882:AAHc4n7whOcjw-BQhKry1X20Aqedxj9nGvM')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')

JULES_BASE_URL = "https://jules.googleapis.com/v1alpha"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
