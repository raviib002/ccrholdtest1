from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'ccrh1' # Must be replaced by your <storage_account_name>
    account_key = 'GYHwEceuHYwDlbuMMENHstLSVJeLxVxSKv7YUe1TAcCRNK1LUTtFSAm0IsKPp6c8v5Y6c4e/sUjo+WkWkf+XSA==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'ccrh1' # Must be replaced by your storage_account_name
    account_key = 'GYHwEceuHYwDlbuMMENHstLSVJeLxVxSKv7YUe1TAcCRNK1LUTtFSAm0IsKPp6c8v5Y6c4e/sUjo+WkWkf+XSA==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
