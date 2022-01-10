# Teacher Directory

## Installation

1. Git clone this repository

```bash
    git clone https://github.com/tanseersaji/teacher_directory_assignment.git
```

2. Install dependencies

First, create a virtual environment so that this project dependencies won't interfere with other projects.

```bash
    pip install virtualenv
```

```bash
    virtualenv -p python3 env
```
    
Then, activate the virtual environment.

In Mac or Linux

```bash
    source env/bin/activate
```

In Windows,

```bash
    .\env\Scripts\activate
```

Finally install the dependencies.

```bash
    pip install -r requirements.txt
```

## Run the server

```bash
    python manage.py runserver 127.0.0.1:8000
```

You can access the platform at http://127.0.0.1:8000/
