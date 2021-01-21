# nagios_probes
check_db.py

Requires pymysql and pyyaml installed on the nagios user profile.

This script works with the check_db_conf.yaml for the database informations.
The script connects to the database with the information given and execute the query.
The results interpretation may require adaptation to give the state desired.

The probe actually tests the amount of comments in the last 4 hours and alerts if they are above 4.
