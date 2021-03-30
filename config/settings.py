SERVER_PORT = 8080
SERVER_DOMAIN = "localhost"
SERVER_EMAIL = "example@example.com"
SERVER_BASE = "http://127.0.0.1:8080/"

LOGS_PATH = "server-logs/"
TEMPLATES_PATH = "templates/"
STATIC_PATH = "static/"
TMP_PATH = "tmp/"
DEFAULT_DOCUMENT = "index.html"

X_POWERED_BY = True
ALLOW_SYMLINKS = False

ALLOW_TEMPLATE_EXEC = True
ALLLOW_TEMPLATE_SYSTEM = True

CORS_ENABLED = True
CORS_CREDENTIALS = False
CORS_ORIGIN = "localhost"

FRAME_OPTIONS = "Deny"
ALLOWED_HOSTS = []

XSS_PROTECTION_HEADER = True
XSS_PROTECTION_MODE = "block"
XSS_PROTECTION_REPORT_URI = False

BLOCKED_PATHS = [
    '/admin',
    '/static/css'
]