MedJellyDataBackend
===================

Backend of MedJellyData mobile apps

# Importing sightings from Proteccion Civil:

./manage.py import_proteccion_civil [--dump-path=<path>] [--auto-export]

This is a command being run every 15 mins, defined in medjellydata's crontab.

# Importing beaches from Proteccion Civíl:

./manage.py import_beaches_from_proteccion_civil

It will create new Proteccion Civil beaches if there are new ones, and it will report name changing, without applying it.

When a new Proteccion Civíl beach has been created, it has to be related with ONE beach. You can do that in admin site.

# Importing beaches from MedJelly:

./manage.py import_medjelly_beaches

It will create new MedJelly beaches if there are new ones, and it will report name changing, without applying it.

When a new MedJelly beach has been created, it has to be related with ONE beach. You can do that in admin site.