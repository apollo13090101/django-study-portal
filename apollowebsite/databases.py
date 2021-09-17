from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== SQLite ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# # ========== PostgreSQL ==========
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# # ========== MySQL ==========
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '',
#         'USER': 'root',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# # ========== MSSQL SERVER ==========
# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'databasename',
#         'USER': 'username',
#         'PASSWORD': 'password',
#         'HOST': 'servername',
#         'PORT': '',

#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
# }

# # Set this to False if you want to turn off pyodbc's connection pooling
# DATABASE_CONNECTION_POOLING = False
