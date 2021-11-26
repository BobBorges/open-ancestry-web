import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/mnt/RAID_34/open-ancestry-web')
sys.path.append('/mnt/RAID_34/open-ancestry-web/ancestry_web')
sys.path.append('/mnt/RAID_34/open-ancestry-web/ancestry_web/ancestry_web')



os.environ['DJANGO_SETTINGS_MODULE'] = 'ancestry_web.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


