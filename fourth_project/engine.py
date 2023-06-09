import time
import random


class Engine():
    def __init__(self, name):

        self.name = f'Engine {name}'
        self.status = 0
        self.enginge_temperature = 0
        self.stop_cycle = False
        self.shaft_noise = 0
        self.log_info = ""
        self.noise = 0
        self.shaft_spin = 0
        self.current_action = ""
        self.engine_mode = 0

    def temp_noise(self, mode):
        if mode == "start":
            random_number = random.randint(0, 200)
            if random_number == 0:
                self.noise = random.randint(-3, 5)
        elif mode == "cycle":
            random_number = random.randint(0, 100)
            if random_number == 0:
                self.noise = random.randint(-2, 2)

    def shaft_noise_gen(self, mode):
        if mode == "cycle":
            random_number = random.randint(0, 100)
            if random_number == 0:
                self.shaft_noise = random.randint(-2, 2)

    def serious_accident(self, temperature):
        if temperature > 150:
            random_number = random.randint(0, 10000)
            if random_number == 10:
                self.noise = random.randint(100, 300)

    def write_temperature(self):
        with open("fourth_project/logs/temp_log.txt", "a") as file:
            file.write(f"{self.enginge_temperature}\n")

    def write_shaft_spin(self):
        with open("fourth_project/logs/shaft_log.txt", "a") as file:
            file.write(f"{self.shaft_spin}\n")

    def engineStart(self):
        self.log_info = "Engine has started"
        while True:
            self.log_info = "Engine is starting"
            self.current_action = "Starting"
            self.enginge_temperature += 2
            self.shaft_spin += 4
            self.temp_noise('start')
            self.noise = 0
            time.sleep(0.1)

            self.accident_check(self.enginge_temperature)
            self.write_temperature()
            self.write_shaft_spin()

            # print(self.enginge_temperature, self.log_info,
            #      self.status, self.current_action, self.engine_mode)

            if self.enginge_temperature >= 150:         # ustawienie temp gap na 180-200
                self.status = 0
                self.engine_mode = 1
                break
        self.engineCycle()

    def engineCycle(self):
        self.log_info = "Engine cycle"
        while True:
            self.current_action = "Working"
            self.temp_noise('cycle')
            self.shaft_noise_gen('cycle')
            if self.status != 2:
                self.serious_accident(self.enginge_temperature)
            self.enginge_temperature += self.noise
            self.shaft_spin += self.shaft_noise
            self.noise = 0
            self.shaft_noise = 0
            self.accident_check(self.enginge_temperature)
            self.write_temperature()
            self.write_shaft_spin()
            # print(self.enginge_temperature, self.log_info,
            #      self.status, self.current_action, self.engine_mode, self.noise)

            if self.stop_cycle == True:
                break

    def stop_engine(self):
        self.stop_cycle = True

    def accident_check(self, temperature):
        if temperature > 190 and temperature < 400:
            self.status = 1
            self.log_info = "Engine overheated"
            self.noise = 0
            self.cooling()

        elif temperature >= 400:
            self.status = 2
            self.log_info = "Critical temperature, emergency shutdown"
            self.noise = 0
            self.cooling()
            self.stop_cycle = True
        else:
            self.log_info = "Temperature OK"

    def cooling(self):
        self.current_action = "Cooling"
        if self.status == 1:
            while self.enginge_temperature > 190:
                self.enginge_temperature -= random.randint(0, 10)
                #self.shaft_spin -= random.randint(0, 10)
                time.sleep(0.1)
                self.write_temperature()
            self.status = 0

        elif self.status == 2:
            while self.enginge_temperature > 30:
                self.enginge_temperature -= random.randint(20, 40)
                self.shaft_spin -= random.randint(20, 40)
                time.sleep(0.7)
                self.write_temperature()
            self.status = 0
            self.log_info = "Work stopped. Sustaining engine"
            self.current_action = "Sustain"


#engine_1 = Engine(1)
# engine_1.engineStart()
#print(engine_1.enginge_temperature, engine_1.status)
