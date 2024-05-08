import properties as prp
from dataclasses import dataclass


JFViewerOutputs = [
    prp.sim_time_s,
    prp.altitude_sl_ft,
    prp.altitude_agl_ft,
    prp.lat_geod_deg,
    prp.lng_geoc_deg,
    prp.roll_rad,
    prp.pitch_rad,
    prp.heading_deg,
    prp.u_fps,
    prp.v_fps,
    prp.w_fps,
    prp.dist_from_start_lat_mt,
    prp.dist_from_start_lon_mt]
