class Car:
    def __init__(self, car_code="", car_name="", car_capacity=0, car_weight=0, car_horsepower=0, car_type=""):
        self.car_code = car_code
        self.car_name = car_name
        self.car_capacity = car_capacity
        self.car_weight = car_weight
        self.car_horsepower = car_horsepower
        self.car_type = car_type

    def __str__(self):
        return (f"{self.car_code}, {self.car_name}, {self.car_capacity}, "
                f"{self.car_weight}, {self.car_horsepower}, {self.car_type}")

    def probationary_licence_prohibited_vehicle(self):
        power_to_mass_ratio = round(self.car_horsepower / self.car_weight) * 1000
        return power_to_mass_ratio > 130

    def found_matching_car(self, car_code):
        return self.car_code == car_code

    def get_car_type(self):
        return self.car_type
