import time
import flypywire as fp
import flypywire.unityapi as unity

client = unity.Client()

a320 = unity.GameObject("Aircrafts/A320", "main-aircraft")
gripen = unity.GameObject("Aircrafts/Gripen", "fighter-jet")
target = unity.GameObject("StaticObjects/sphere", "target")


with client.RenderContext() as ctx:
    
    ctx.set_origin(geoloation = unity.Geolocation())
    
    ctx.spawn_gameobject(a320, geolocation = unity.Geolocation(10.032, -12.012, 1000))
    ctx.spawn_gameobject(gripen, relative_to = a320, transform = unity.Transform(unity.Vector(10, 0, 0)))
    ctx.spawn_gameobject(target, parent = a320, transform = unity.Transform(unity.Vector3(0, 0, -10), unity.Vector3(30, 0, 0)))
    
    while True:

        a320_state = fp.AircraftState(
            latitude = 0.0,
            longitude = -10,
            height = 1000,
            roll_rad = 0.0,
            pitch_rad = 0.0,
            yaw_rad = 0.0,
            landing_gear = True,
            engines = "Running")
        
        
        ctx.simulation_state = fp.SimulationState(
            timestamp = time.time(),
            aircrafts = {a320.name : a320_state})
        
        ctx.publish_simulation_state(delta_time = 0.1) ##Use time.sleep(delta_time) inside here or something like that

        
