class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def calculate(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        if output > 50:
            output = 50
        if output < -50:
            output = -50
        if error > 200:
            output = 60
        if error < -200:
            output = -60
        if output < 0:
            output = output - 13
        else:
            output = output + 13
        print("output", output)
        return output