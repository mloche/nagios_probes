#!/bin/python3

from random import randint
import sys
import pymysql as mariadb


#UNKNOWN = 3
#OK = 0
#WARNING = 1
#CRITICAL = 2

db_serv=sys.argv[1]
db_name=sys.argv[2]
db_user=sys.argv[3]
db_password=sys.argv[4]
query="SELECT COUNT(*) FROM wp_comments WHERE comment_date > DATE_SUB(NOW(),INTERVAL 4 HOUR);"
status_code=-1

### Connecting to database returns connector ### 
def _connect(db_serv,db_admin,db_pass,db_name,db_port=3306):
	if isinstance(db_serv, str) and isinstance(db_admin,str) and isinstance(db_pass,str) and isinstance(db_name,str) and isinstance(db_port,int):
		try:
			conn = mariadb.connect(host=db_serv,user=db_admin,password=db_pass,database=db_name,port=db_port)
		except mariadb.Error as error:
			print("error connecting to mariadb platform: {} with _connect".format(error))
			return(False)
	else:
		sys.stdout.write("Unknown state for DB ")
		status_code=3
	return(conn)

### Query database, requires connector and query, returns query result ###
def _query(conn,query):
	if  isinstance(query,str) and isinstance(conn, mariadb.connections.Connection):
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			data_query = cursor.fetchone()
		except:
			sys.stdout.write("Unknown state for DB ")
			status_code=3
	else:
		sys.stdout.write("Unknown state for DB ")
		status_code=3
	return(data_query)



connector=_connect(db_serv,db_user,db_password,db_name)

comments_number=int(_query(connector,query)[0])
#control print(type(comments_number),comments_number)


if comments_number < 4:
	status_code==0
	sys.stdout.write("OK :: Comments volume is normal, less than 1 per hour")
elif comments_number > 4 and comments_number < 10:
	status_code==1
	sys.stdout.write("WARNING :: comments volume is rapidly increasing, more than 1 per hour")
elif comments_number < 10 :
	status_code==2
	sys.stdout.write("Critical :: comments volume important, more than 2 per hour")
else:
	status_code== 3
	sys.stdout.write("Unknown state for comments status")

#control print(status_code)
sys.exit(status_code)
