"""Default settings."""

import logging
import os
import environ

# reading the env file
env = environ.Env()
environ.Env.read_env()

#
# Development mode or production mode
# If DEBUG is True, then auto-reload is enabled, i.e., when code is modified, server will be
# reloaded immediately
#
DEBUG = True

#
# Static Assets
#
# The web UI is a single page app. All javascripts/css files should be in STATIC_DIR_PATH
#
STATIC_DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
TEMPLATE_DIR_PATH = STATIC_DIR_PATH
APP_INDEX_PAGE = 'index.html'

#
# Server setup
#
HTTP_PORT = 7777
HTTP_ADDRESS = '0.0.0.0'

TORNADO_MAX_WORKERS = 8

#
# ApScheduler settings
#
THREAD_POOL_SIZE = 4
JOB_MAX_INSTANCES = 3
JOB_COALESCE = True
TIMEZONE = 'UTC'

# When a job is misfired -- A job were to run at a specific time, but due to some
# reason (e.g., scheduler restart), we miss that run.
#
# By default, if a job is misfired within 1 hour, the scheduler will rerun it.
# Otherwise, if it's misfired over 1 hour, the scheduler will not rerun it.
JOB_MISFIRE_GRACE_SEC = 3600

#
# Database settings
#
JOBS_TABLENAME = 'scheduler_jobs'
EXECUTIONS_TABLENAME = 'scheduler_execution'
AUDIT_LOGS_TABLENAME = 'scheduler_jobauditlog'

DATABASE_TABLENAMES = {
    'jobs_tablename': JOBS_TABLENAME,
    'executions_tablename': EXECUTIONS_TABLENAME,
    'auditlogs_tablename': AUDIT_LOGS_TABLENAME
}

# See different database providers in mainspring/core/datastore/providers/
DATABASE = env("DATABASE", "MySQL")
if DATABASE == "Postgres":
    # Postgres
    DATABASE_CLASS = 'mainspring.core.datastore.providers.postgres.DatastorePostgres'
    DATABASE_CONFIG_DICT = {
        'user': env("DB_USER"),
        'password': env("DB_PASS"),
        'hostname': env("DB_HOST"),
        'port': env("DB_PORT", 5432),
        'database': env("DB_NAME", "argon-scheduler"),
        'sslmode': 'disable'
    }
elif DATABASE == "MySQL":
    # MySQL
    DATABASE_CLASS = 'mainspring.core.datastore.providers.mysql.DatastoreMySQL'
    DATABASE_CONFIG_DICT = {
        'user': env("DB_USER", "airisbad"),
        'password': env("DB_PASS", "lukeffUdnoodPhosDilHuif6"),
        'hostname': env("DB_HOST", "ascent-it.cijfstakmq3t.ap-south-1.rds.amazonaws.com"),
        'port': env("DB_PORT", 3306),
        'database': env("DB_NAME", "argon-scheduler"),
    }
elif DATABASE == "Sqlite":
    # Sqlite
    DATABASE_CLASS = 'mainspring.core.datastore.providers.sqlite.DatastoreSqlite'
    DATABASE_CONFIG_DICT = {
        'file_path': 'datastore.db'
    }

# RABBITMQ
#
RABBIT_CONFIG_DICT = {
    'host': env("RABBIT_HOST"),
    'port': env("RABBIT_PORT"),
    'username': env("RABBIT_USER"),
    'password': env("RABBIT_PASS")
}

# mainspring is based on apscheduler. Here we can customize the apscheduler's main scheduler class
# Please see mainspring/core/scheduler/base.py
SCHEDULER_CLASS = 'mainspring.core.scheduler.base.SingletonScheduler'

#
# Set logging level
#
logging.getLogger().setLevel(logging.INFO)


# Packages that contains job classes, e.g., simple_scheduler.jobs
JOB_CLASS_PACKAGES = []
