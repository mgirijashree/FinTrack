import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fintrack.settings')

application = get_wsgi_application()