# flake8: noqa
from .settings import *

DEBUG = False
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.getenv('blobforccrh')
AZURE_CONTAINER = os.getenv('AZ_STORAGE_CONTAINER')
AZURE_ACCOUNT_KEY = os.getenv('+sYzKcLXQLvtefDkSAEONpc346QUUKJOyS/DU126ACzB+czxeZedGBSYxP1tC0QockYCzINydntJBLfPn9bvVQ==')
