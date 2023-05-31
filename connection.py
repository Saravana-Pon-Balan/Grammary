import ibm_db

def connect_to_database():
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;sslCAFile=1dd14d0c-1b52-4f63-a606-53ecba28771d;PROTOCOL=TCPIP;UID=lss04391;PWD=In33dla2jcabKkEK;","","")
    return conn
