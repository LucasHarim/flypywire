from collections import deque
import numpy as np


class PIDController:

    def __init__(self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        dt: float = 0.03):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
    
        self.error_buffer = deque(maxlen=10)

    def run_step(self, target: float, current: float) -> float:

        error = target - current
        self.error_buffer.append(error)

        if len(self.error_buffer) >= 2:
            _de = (self.error_buffer[-1] - self.error_buffer[-2]) / self.dt
            _ie = sum(self.error_buffer) * self.dt

        else:
            _de = 0.0
            _ie = error * self.dt
        
        val = self.kp * error + self.ki * _ie + self.kd * _de
        
        return np.clip(val, -1, 1)