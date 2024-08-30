from flypywire import (
    Publisher,
    Subscriber,
    SimulationState,
    AircraftState)

if __name__ == '__main__':

    pub = Publisher(debug=False)
    sub = Subscriber(debug = True)
    sub.start_listening()

    time = 0
    
    while True:

        aicraft_state = AircraftState(time, 0, 1000, 0, 0, 0, foo = True, landing_gear = False)

        sim_state = SimulationState(time, aircrafts={'my-aircraft': aicraft_state})
        pub.publish_simulation_state(sim_state)

        time += 1

        if sub.is_data_available:

            sub.get_simulation_state()
            
            

        

            
        
            
