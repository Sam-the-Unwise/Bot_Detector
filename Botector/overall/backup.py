from sshtunnel import SSHTunnelForwarder
#import paramiko
import pymongo
import pprint
import pysftp

# create SSH tunnel

SERVER_HOST = "tunnel-ssh"
SERVER_PASS = "!d4t42oi8*"

LOGIN_HOST = "remotepc-ssh"
LOGIN_PASS = "d4c0m2oi7!" 


server = SSHTunnelForwarder(
    SERVER_HOST,
    #ssh_username="pahaz",
    ssh_password = SERVER_PASS,
    remote_bind_address=('127.0.0.1', 8080)
)

try:
    server.start()

    print("Connected to SSH Tunnel with local bind port %s" %server.local_bind_port)  # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.
    
    
    # establish remote connection
    try:

        print("\nEstablishing connection to %s" %LOGIN_HOST)

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys.load = ("known_hosts")
        with pysftp.Connection(LOGIN_HOST, password = LOGIN_PASS, cnopts = cnopts) as sftp:
             print("CONNECTED")

        #client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
        #db = client[MONGO_DB]
        #pprint.pprint(db.collection_names())

    except:
        print("Unable to connect")
        pass

    server.stop()
    print("\nServer stopped. Goodbye")

except:
    print("Could not connct")
    pass








# save data from mongoDB in a list or something


# stop SSH tunnel


# analyze data
    # compare comments to see if they are similar
        # create a system that keeps track of how many similar comments this "user" has made
    # if most/all comments are similar, set user = bot to TRUE

# discover if user is a bot or not
