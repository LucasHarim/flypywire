from collections import deque
import numpy as np

class PIDController:

    def __init__(self,
        K_P: float = 1.0,
        K_I: float = 0.0,
        K_D: float = 0.0,
        dt: float = 0.03):

        self.K_P = K_P
        self.K_I = K_I
        self.K_D = K_D
        self.dt = dt
        
        self._error_buffer = deque(maxlen=10)

    def run_step(self, target: float, current_value: float) -> float:

        error = target - current_value
        self._error_buffer.append(error)

        if len(self._error_buffer) >= 2:
            _derivative = (self._error_buffer[-1] - self._error_buffer[-2]) / self.dt
            _integral = sum(self._error_buffer) * self.dt
        
        else:
            _derivative = 0.0
            _integral = 0.0
        
        value = self.K_P * error + self.K_I * _integral + self.K_D * _derivative

        return np.clip(value, -1, 1)
