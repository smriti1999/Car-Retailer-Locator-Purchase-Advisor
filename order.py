import random
import string


class Order:
    def __init__(self, order_id="", order_car=None, order_retailer=None, order_creation_time=0):
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = order_creation_time

    def __str__(self):
        return f"{self.order_id}, {self.order_car}, {self.order_retailer}, {self.order_creation_time}"

    def generate_order_id(self, car_code):
        # Step 1: Generate a random string of 6 lowercase alphabetic characters
        random_string = ''.join(random.choices(string.ascii_lowercase, k=6))

        # Step 2: Convert every second character to uppercase
        modified_string = ''.join(
            char.upper() if i % 2 == 1 else char for i, char in enumerate(random_string))

        # Step 3: Get the ASCII code of each character
        ascii_codes = [ord(char) for char in modified_string]

        # Step 4: Calculate the ASCII code to the power of 2 and get the remainder
        str_1 = "~!@#$%^&*"
        powered_codes = [(code ** 2) % len(str_1) for code in ascii_codes]

        final_string = ''.join(str_1[powered_codes[idx]] * idx for idx in range(len(powered_codes)))

        # Step 6: Append each character n times to the modified string
        return modified_string + final_string + car_code + str(self.order_creation_time)
