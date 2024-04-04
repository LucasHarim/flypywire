from jsbsimpy.fdm_pubsub import FDMSubscriber

if __name__ == "__main__":
    
    sub = FDMSubscriber(host = "tcp://127.0.0.1", port = 5555, topic = "", debug = True)

    while True:

        fdm_msg = sub.rcv_fdm_outputs()
        if fdm_msg != None: print(fdm_msg)