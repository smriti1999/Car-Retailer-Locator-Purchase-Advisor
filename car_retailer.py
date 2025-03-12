from retailer import Retailer
from car import Car
from order import Order
import time
import random


class CarRetailer(Retailer):
    retailer_stock = []

    def __init__(self, retailer_id=-1, retailer_name="", carretailer_address="", carretailer_business_hours=(),
                 carretailer_stock=None):
        super().__init__(retailer_id, retailer_name)
        if carretailer_stock is None:
            carretailer_stock = []
        self.carretailer_address = carretailer_address
        self.carretailer_business_hours = carretailer_business_hours
        self.carretailer_stock = carretailer_stock
        self.load_current_stock("../data/stock.txt")

    def __str__(self):
        return (f"{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, "
                f"{self.carretailer_business_hours}, {self.carretailer_stock}")

    def load_current_stock(self, path):
        try:
            with open(path, "r") as stock_file:
                data = stock_file.readlines()
                codes = []
                cars = []
                for line in data:
                    if int(line[0:8]) == self.retailer_id:
                        st_idx = line.index("[")
                        end_idx = line.index("]")
                        car_info = line[st_idx + 1: end_idx]
                        for detail in eval(car_info):
                            car = detail.split(", ")
                            cars.append(Car(car[0], car[1], int(car[2]), int(car[3]), int(car[4]), car[5]))
                            codes.append(car[0])
            stock_file.close()
            self.retailer_stock = cars
            self.carretailer_stock = codes
        except Exception as e:
            print(f"Error while loading stock data: {e}")
            return []

    def is_operating(self, cur_hour):
        hours = self.carretailer_business_hours.strip('()').split(',')
        return float(hours[0]) <= cur_hour <= float(hours[1])

    def get_all_stock(self):
        return self.retailer_stock

    def get_postcode_distance(self, postcode):
        postcode_data = self.carretailer_address.split(", ")
        postcode_str = ''.join(filter(str.isdigit, postcode_data[1]))
        postcode_int = int(postcode_str)
        return abs(postcode_int - postcode)

    def remove_from_stock(self, car_code):
        for car in self.retailer_stock:
            if car.car_code == car_code:
                del self.retailer_stock[self.retailer_stock.index(car)]
                self.file_updation()
                return True
        return False

    def add_to_stock(self, car):
        if car.car_code in self.carretailer_stock:
            return False
        else:
            self.retailer_stock.append(car)
            self.file_updation()
            return True

    def get_stock_by_car_type(self, car_types):
        cars = []
        for car in self.retailer_stock:
            if car.get_car_type() in car_types:
                cars.append(car)
        return cars

    def get_stock_by_licence_type(self, licence_type):
        stock = self.get_all_stock()
        if licence_type == "P":
            matching_cars = [car for car in stock if car.probationary_licence_prohibited_vehicle()]
            return matching_cars
        else:
            return self.retailer_stock

    def car_recommendation(self):
        if len(self.retailer_stock) > 0:
            random_car_code = random.choice(self.retailer_stock)
            return random_car_code
        else:
            return None

    def create_order(self, car_code):
        current_time = time.localtime().tm_hour + round(time.localtime().tm_min / 60, ndigits=1)
        if not self.is_operating(current_time):
            print("Sorry, the retailer is currently closed. Please place your order during business hours.")
            return None
        self.remove_from_stock(car_code)
        order = Order("", car_code, self.retailer_id, int(time.time()))
        order.generate_order_id(car_code)
        return order

    def file_updation(self):
        data = []
        with open("../data/stock.txt", "r") as stock_file:
            lines = stock_file.readlines()
            for line in lines:
                retailer_id = int(line[0:8])
                if retailer_id == self.retailer_id:
                    cars = [car.__str__() for car in self.retailer_stock]
                    retailer = line.split(", ")
                    updated_string = ", ".join(retailer[0:6]) + ", " + str(cars)
                    data.append(updated_string)
                else:
                    data.append(line)
        with open("../data/stock.txt", "w") as stock_file:
            stock_file.write("\n".join(data))
        stock_file.close()
