from jsbsimpy.fdm_pubsub import FDMSubscriber

if __name__ == "__main__":
    
    sub = FDMSubscriber(host = "tcp://127.0.0.1", port = 2000, topic = "")

    sub.start_listening()

    while True:
        
        if sub.is_data_available:
            fdm_msg = sub.get_fdm_outputs()
            print(fdm_msg)
        