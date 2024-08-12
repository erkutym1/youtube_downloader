# your_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

import celery.app.amqp
import celery.app.log
import celery.worker.autoscale
import celery.worker.components
import celery.bin
import celery.utils
import celery.utils.dispatch
import celery.contrib.testing
import celery.utils.static
import celery.concurrency.prefork
import celery.app.events
import celery.events.state
import celery.app.control
import celery.backends.redis
import celery.backends
import celery.backends.database
import celery.worker
import celery.worker.consumer
import celery.app
import celery.loaders
import celery.security
import celery.fixups
import celery.concurrency
import celery.events
import celery.contrib
import celery.apps
import celery
import celery.fixups
import celery.fixups.django
import celery.apps.worker
import celery.worker.strategy
import kombu.transport.redis
import sqlalchemy.sql.default_comparator
import sqlalchemy.ext.baked

# 'celery' programı için varsayılan Django ayar modülünü ayarlayın.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tubdown.settings')

app = Celery('tubdown')

# Bu şekilde bir string kullanmak, işçinin yapılandırma nesnesini çocuk süreçlerine serileştirmesine gerek kalmaz.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm kayıtlı Django uygulama yapılandırmalarından görev modüllerini yükleyin.
app.autodiscover_tasks()
