import time
import flypywire as fpw
from flypywire import unityapi as unity

if __name__ == '__main__':

    client = unity.Client()
    origin = unity.GeoCoordinate(-22.951804,  -43.210760, 1000) #Cristo redentor

    with client.RenderContext() as ctx:
        
        assets = ctx.get_assets_library()
        
        for asset_path in assets:
            
            print(asset_path)
            
            actor = unity.Actor('main-actor', asset_path)
            ctx.spawn_actor(actor, origin)
            
            time.sleep(4)
            ctx.destroy_actor(actor)