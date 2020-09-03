#from django.conf import settings
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'ccrhhot' # Must be replaced by your <storage_account_name>
    account_key = 'hSl5OWt2U0wuOwIKWCUW/2vJxA3Qm3P+SW5HPMCkYT3h46K5UluPzTqzLe5jaj0q61uUIzxNyPVzV80aPGibwg==' # Must be replaced by your <storage_account_key>
    azure_container = 'ccrhmedia'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'ccrhhot' # Must be replaced by your storage_account_name
    account_key = 'hSl5OWt2U0wuOwIKWCUW/2vJxA3Qm3P+SW5HPMCkYT3h46K5UluPzTqzLe5jaj0q61uUIzxNyPVzV80aPGibwg==' # Must be replaced by your <storage_account_key>
    azure_container = 'ccrhstatic'
    expiration_secs = None
