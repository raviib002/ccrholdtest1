#from django.conf import settings
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'ccrhstaticfiles' # Must be replaced by your <storage_account_name>
    account_key = 'eOYVAq+sn0mHR3YG0RFlMXde5su5Hdfjo/kWziqPPBih7P3YjTsaQsoKe/KNZpvhzBfQ0dJGUlLXHmSWfJaSCA==' # Must be replaced by your <storage_account_key>
    azure_container = 'ccrhmedia'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'ccrhstaticfiles' # Must be replaced by your storage_account_name
    account_key = 'eOYVAq+sn0mHR3YG0RFlMXde5su5Hdfjo/kWziqPPBih7P3YjTsaQsoKe/KNZpvhzBfQ0dJGUlLXHmSWfJaSCA==' # Must be replaced by your <storage_account_key>
    azure_container = 'ccrhstatic'
    expiration_secs = None
