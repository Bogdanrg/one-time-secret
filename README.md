One Time Secret app.
Provides you opportunity to share your important secrets securly

Implemented two routes: 
1. /generate - expects three arguments: your secret; secret phrase which knows person who will receive 
it; lifetime of your secret in seconds (default 3600 sec). You will receive an URL, containing secret key.
2. /secrets/{secret_key} - secret_key is a string which you received from the /generate route. Expects a secret phrase,
if the secret phrase is correct and the secret isn't expired you will see it, then it will be deleted.

Your secrets and secret phrases are stored in encrypted form, so you can be calm about your data. 
