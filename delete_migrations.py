import os

apps_path = 'apps'

for app in os.listdir(apps_path):
    app_migrations_path = os.path.join(apps_path, app, 'migrations')