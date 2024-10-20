import cv2
import flypywire as fp
import flypywire.unityapi as unity
from flypywire.control import PIDController
from flypywire.jsbsim_fdm import properties as prp

import numpy as np
from random import choice
from fdm_setup import get_fdm

deg2rad = np.pi/180
origin = unity.GeoCoordinate(-22.951804,  -43.210760, 1000) #Cristo redentor
DT = 0.03

glider = get_fdm(origin, DT)

client = unity.Client()


with client.RenderContext() as ctx:
    
    for a in ctx.get_assets_library():
        print(a)

    ctx.set_origin(origin)
    main_actor = unity.GameObject('main-actor', 'Assets/UAVs/FixedWing01')
    # main_actor = unity.GameObject('main-actor', 'Assets/Gliders/Glider01')
    ctx.spawn_gameobject(main_actor, geocoordinate=origin)
    
    # ctx.spawn_camera('main-cam', main_actor, transform = unity.Transform(unity.Vector3(0, 2, -5)))
    # ctx.spawn_camera('main-cam', main_actor, transform = unity.Transform(unity.Vector3(0, -0.35, -0.25)))
    # cam = unity.Camera(port = 2000)

    balloons = [asset for asset in ctx.get_assets_library() if 'HotAir' in asset]
    num_balloons = 10
    rolenames = [f'b[{i}]' for i in range(num_balloons)]
    
    geocoordinates = [unity.GeoCoordinate(
            origin.latitude + 8e-3 * np.random.normal(),
            origin.longitude + 8e-3 * np.random.normal(),
            origin.height_m + 100 * np.random.normal()) for _ in range(num_balloons)]
    
    for i, name in enumerate(rolenames):
        ctx.spawn_gameobject(unity.GameObject(name, choice(balloons)), geocoordinate=geocoordinates[i])

    u = 1e-5 * np.random.normal(size = num_balloons) + 1e-6
    v = 1e-5 * np.random.normal(size = num_balloons) + + 1e-6
    w = 0.1 * np.random.normal(size = num_balloons) + 0.01

    attitude_controller = PIDController()
    roll_controller = PIDController()
    
    dt = DT
    sim_time = 0

    while True:
        
        glider[prp.elevator_cmd()] = - attitude_controller.run_step(2 * deg2rad, glider[prp.pitch_rad()])
        
        if 10 < glider[prp.sim_time_s()] < 20:
            roll_target = 30*deg2rad
            
        else:
            roll_target = 0
        
        roll_cmd = roll_controller.run_step(roll_target, glider[prp.roll_rad()])
        glider[prp.aileron_cmd()] = roll_cmd
        glider[prp.rudder_cmd()] = -0.5*roll_cmd

        geocoordinates = [
            unity.GeoCoordinate(
                geocoordinates[i].latitude + u[i] * dt,
                geocoordinates[i].longitude + v[i] * dt,
                geocoordinates[i].height_m + w[i] * dt) for i in range(num_balloons)]
        
        
        states = [fp.ActorState(
            float(geocoordinates[i].latitude),
            float(geocoordinates[i].longitude),
            float(geocoordinates[i].height_m),
            0, 0, 0) for i in range(num_balloons)]
        
        # cam.imshow()
        ctx.publish_simulation_state(
            fp.SimulationState(sim_time, 
                {main_actor.name: fp.get_aircraft_state_from_fdm(glider),
                **{rolenames[i]: states[i] for i in range(num_balloons)}}),
            dt)
        
        glider.run()
        sim_time += dt

        # if cam.img_available:
        #     frame = cam.get_image()
        #     effect = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     cv2.imshow('Camera', effect)
            
        #     if cv2.waitKey(1) == ord('q'):
        #         break




