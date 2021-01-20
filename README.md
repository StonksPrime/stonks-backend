# stonks backend

Installation
============

1. Create python virtual environment
    ```bash
    python3 -m venv myvenv
    ```

2. Activate virtual environment
    ```bash
	source myvenv/bin/activate
    ```

3. Install requirements
    ```bash
    pip install -r requirements.txt 
    ```

4. Install postgresql and configure it replacing this code 
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'stonksDB',
            'USER': 'username',
            'PASSWORD': 'password-changeme',
            'HOST': '127.0.0.1',
            'PORT': '',
          }
    }
    ```

5. Apply database migration
    ```bash
    python manage.py migrate
    ```
