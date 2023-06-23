# import sqlalchemy
# import pymysql
# import mysql.connector


# from sqlalchemy import create_engine, text, DateTime




# engine = create_engine(
#     "mysql+pymysql://s31fjunidh21tdjjjlj7:pscale_pw_zmPBPepM8Yb5eyPLUHVANBKyDhQrnm1IvTY4qJh6eyh@aws.connect.psdb.cloud/finder_database",
#     connect_args={
#         "ssl": {
#             "ca": "/etc/ssl/cert.pem",
           
#         }
#     }
# )
# # pymysql.connect(host="aws.connect.psdb.cloud", 
# #                 port=3306, user="s31fjunidh21tdjjjlj7",
# #                 password="pscale_pw_zmPBPepM8Yb5eyPLUHVANBKyDhQrnm1IvTY4qJh6eyh", database="finder_database")

# #connect python with clouddatabase
# database_connection = mysql.connector.connect(host="aws.connect.psdb.cloud", 
#                 port=3306, user="s31fjunidh21tdjjjlj7",
#                 password="pscale_pw_zmPBPepM8Yb5eyPLUHVANBKyDhQrnm1IvTY4qJh6eyh", database="finder_database")

# #get cursor object
# cursor = database_connection.cursor()

# #execute query
# cursor.execute("select * from user")

# #fetch all matching rows
# result = cursor.fetchall()

# for row in result:
#     print(row)
#     print(type(result))
    
# print(database_connection)

# # with database_connection.connect() as conn:
# #     result = conn.execute(text("select * from userlogin"))
# #     print(type(result))