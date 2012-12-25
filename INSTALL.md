# Installation Instructions

Please follow these instructions to get this application set up!

First set up MySQL. Make sure you have a user with access to a database for the application, and that the credentials and information match what is in `aphfta/settings.py`

Then load the schema:

```bash
python manage.py syncdb
```

Finally, you can seed your database by loading data from fixtures:

```bash
python manage.py loaddata fixtures/*
```
