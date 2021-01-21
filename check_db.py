#!/bin/python3

import sys
import pymysql 
import yaml


#Reminder #
#UNKNOWN = 3
#OK = 0
#WARNING = 1
#CRITICAL = 2


### Function reading the yaml file and extracting the data ####

def import_yaml_file(file):
	if isinstance(file, str):
#		print("Starting Import yaml")
		try:
			with open(file) as read_file:
				data = yaml.load(read_file, Loader=yaml.FullLoader)
#control				print("Data read are : {}".format(data))
				return(data)
		except Exception as err :
			print("Could not open {} file error : {}".format(file,err))
	else:
		sys.exit("Could not import yaml file : {} is not a valid file or path".format(file))




### Connecting to database returns connector ### 
def _connect(db_serv,db_admin,db_pass,db_name,db_port=3306):
	if isinstance(db_serv, str) and isinstance(db_admin,str) and isinstance(db_pass,str) and isinstance(db_name,str) and isinstance(db_port,int):
		try:
			conn = pymysql.connect(host=db_serv,user=db_admin,password=db_pass,database=db_name,port=db_port)
		except pymysql.Error as error:
			print("error connecting to mariadb platform: {} with _connect".format(error))
			return(False)
	else:
		sys.stdout.write("Unknown state for DB ")
		status_code=3
	return(conn)

### Query database, requires connector and query, returns query result ###
def _query(conn,query):
	if  isinstance(query,str) and isinstance(conn, pymysql.connections.Connection):
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			data_query = cursor.fetchone()
			return(data_query)
		except:
			sys.stdout.write("Unknown state for DB ecept ")
			status_code=3
	else:
		sys.stdout.write("Unknown state for DB else")
		status_code=3
	



####################################################
#              MAIN PROGRAM                        #
####################################################

### Check for a second arguments before anything ###
if len(sys.argv) != 2 :
	raise ValueError("Please provide path to yaml file as argument, usage : {} path ".format(sys.argv[0]))



### STEP 1 : Import YAML file content into yaml_data variable ###

yaml_data=import_yaml_file(sys.argv[1])

### STEP 2 : Import DATABASE connect informations and create connector ###

db_info=yaml_data.get('database').get('database')

connector=_connect(db_info["db_host"],db_info["db_admin"],db_info["db_password"],db_info["db_name"],db_info["db_port"])

### STEP 3 : Import DATABASE query ###

db_query=str(yaml_data.get('database').get('query'))

### STEP 4 : proceed query and return result, this part can be modified acording to personal purposes ###

# query returns a tuple with the desired value as first element #

(comments_number,)=_query(connector,db_query)
#control print("Comments number in the last 4 hours ",comments_number)


if comments_number <= 4:
	status_code=0
	sys.stdout.write("OK :: Comments volume is normal, {} in the last 4 hours\n".format(comments_number))
	#print("status code is :",status_code)
	sys.exit(status_code)
elif comments_number > 4 and comments_number <= 10:
	status_code=1
	sys.stdout.write("WARNING :: comments volume is rapidly increeasing, {} in the last 4 hours\n".format(comments_number))
	#print("status code is :",status_code)	
	sys.exit(status_code)
elif comments_number > 10 :
	status_code=2
	sys.stdout.write("Critical :: comments volume important, {} in the last 4 hours\n".format(comments_number))
	print("status code is :",status_code)
	sys.exit(status_code)
else:
	status_code= 3
	print("status code is :",status_code)
	sys.stdout.write("Unknown state for comments status\n")

#control print(status_code)
	sys.exit(status_code)

