# IRS Copilot API

## Requirements

- Python 3.11

## Install packages

```pip install -r requirements.txt```

## Setup

### Environment Variables 
- Create .env file
- Checkout .env_example file

### Credentials folder
- Create credentials directory
- Checkout credentials_example directory
- Make sure you have firebase credentials json file

### Import HTTP request JSON for [Insomnia](https://insomnia.rest/download) 
- Check out json-requests-exports directory

## Run prod

```gunicorn app:app```

## Run dev
```gunicorn --reload app:app```