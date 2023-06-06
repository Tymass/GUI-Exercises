import time
import random


class Engine():
    def __init__(self, name, shared_dict):

        #self.file.open("engine_data.txt", "a").close()
        self.shared_dict = shared_dict
        self.shared_dict['engine_mode'] = 0
        self.name = f'Engine {name}'
        self.status = 0
        self.enginge_temperature = 0
        self.stop_cycle = False

        self.log_info = ""
        self.error_info = ""
        self.noise = 0
        #self.random_number = 0
        self.shaft_spin = 0
        self.time_step = 0
        self.current_action = ""
        self.engine_mode = 0            # mode 0 is start

    def temp_noise(self, mode):
        if mode == "start":
            random_number = random.randint(0, 200)
            if random_number == 0:
                self.noise = random.randint(50, 60)
        elif mode == "cycle":
            random_number = random.randint(0, 100)
            if random_number == 0:
                self.noise = random.randint(1, 5)

    def serious_accident(self, temperature):
        if temperature > 150:
            random_number = random.randint(0, 900)
            if random_number == 0:
                self.noise = random.randint(100, 300)

    def write_temperature(self):
        with open("engine_data.txt", "a") as file:
            file.write(f"{self.enginge_temperature}\n")

    def engineStart(self):
        self.log_info = "Engine has started"
        self.shared_dict['engine_mode'] = 1
        while True:
            self.log_info = "Engine is starting"
            self.current_action = "Starting"
            self.enginge_temperature += 1
            self.temp_noise('start')
            self.enginge_temperature += self.noise
            time.sleep(0.1)

            self.accident_check(self.enginge_temperature)
            self.write_temperature()
            print(self.enginge_temperature, self.log_info,
                  self.status, self.current_action, self.engine_mode)

            if self.enginge_temperature >= 170:         # ustawienie temp gap na 180-200
                self.status = 0
                self.engine_mode = 1
                break

    def engineCycle(self):
        self.log_info = "Engine cycle"
        while True:
            self.current_action = "Working"
            self.temp_noise('cycle')
            if self.status != 2:
                self.serious_accident(self.enginge_temperature)
            self.enginge_temperature += self.noise
            self.accident_check(self.enginge_temperature)
            self.write_temperature()
            print(self.enginge_temperature, self.log_info,
                  self.status, self.current_action, self.engine_mode, self.noise)

            if self.stop_cycle == True:
                break

        # if self.enginge_temperature < 50 and self.enginge_temperature > 10:
        #    break
        #    self.engineStart()

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
                time.sleep(0.1)
                print(self.noise)
                self.write_temperature()
            self.status = 0
            # print(self.enginge_temperature, self.log_info,
            #      self.status, self.current_action)

        elif self.status == 2:
            while self.enginge_temperature > 30:
                self.enginge_temperature -= random.randint(20, 40)
                time.sleep(0.7)
                print(self.enginge_temperature)
                self.write_temperature()
            self.status = 0

            # print(self.enginge_temperature, self.log_info,
            #      self.status, self.current_action)


#engine_1 = Engine(1)
# engine_1.engineStart()
#print(engine_1.enginge_temperature, engine_1.status)
