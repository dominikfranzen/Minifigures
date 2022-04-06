# Features of Unbrickable

## Auth Process
You need to create a file with the name "auth_credentials.json" in the main folder (the same folder as auth.py) in order to make the API requests work.
The File must have the following structure:
```
{
    "client_key": YOUR_BRICKLINK_CONSUMERKEY,
    "client_secret": YOUR_BRICKLINK_CONSUMERSECRET,
    "resource_owner_key": YOUR_BRICKLINK_TOKENVALUE,
    "resource_owner_secret": YOUR_BRICKLINK_TOKENSECRET
}
```
