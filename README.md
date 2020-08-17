[![Build Status](https://travis-ci.com/Njaya2019/FindHelp-app.svg?branch=develop)](https://travis-ci.com/Njaya2019/FindHelp-app)[![Coverage Status](https://coveralls.io/repos/github/Njaya2019/FindHelp-app/badge.svg?branch=develop)](https://coveralls.io/github/Njaya2019/FindHelp-app?branch=develop)

# FindHelp-app
It's an API where users posts questions and others users may provide answers to the questions. The answers can be upvoted or downvoted, A user can mark an answer as correct, This will help other users to find the correct answers to the questions already asked.

## Language
```
- Python
```

## Version
```
- 3.6
```

## Framework
```
- Flask python framework
```

## DATABASE engine
```
- PostgreSQL
```

## Running API

### Clone the api
```
- git clone git@github.com:Njaya2019/FindHelp-app.git
```

### Change directory to project's root folder
```
- cd FindHelp-app
```

### Set enviroment varibles

#### Set database and test database enviromental variables
```
- DB_URL="dbname=your-database user=postgres host=localhost password=your-password"
- TDB_URL="dbname=your-test-database user=postgres host=localhost password=your-password"
```
#### Set Gmail SMTP and password enviromental variables
```
- EMAIL = "your-gmail"
- EMAIL_PASSWORD = "your-gmail-password"
```

### Install dependancies
```
- pip install requirements.txt
```

### Run the API
```
- python run.py
```

## Running pytest tests
```
- py.test -vv
```

## Collaborators
[Andrew Njaya](https://github.com/Njaya2019)

## References
- [Python](https://docs.python.org/3.6/)
- [Flask framework](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
