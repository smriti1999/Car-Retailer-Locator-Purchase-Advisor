# your imports go here
import os
import random
import string
from car import Car
from car_retailer import CarRetailer


def main_menu():
    print("Car Purchase Advisor System")
    print("1. Look for the nearest car retailer")
    print("2. Get car purchase advice")
    print("3. Place a car order")
    print("4. Exit")


def generate_test_data():
    retailers = []
    test_data = []
    for retailer_range in range(3):
        characters = string.ascii_letters
        retailer_name = ''.join(random.choice(characters) for _ in range(8))
        retailer_address = (f"{random.choice(['Clayton Rd Clayton', 'Clayton Rd Mount Waverley'])}, "
                            f"VIC310{retailer_range}")
        retailer_business_hours = random.choice([(6.0, 8.0), (8.0, 12.0), (12.0, 23.0), (6.0, 23.9)])
        retailer = CarRetailer('', retailer_name, retailer_address, retailer_business_hours)
        retailer.generate_retailer_id(retailers)
        retailers.append(retailer)
        cars = []
        for car_range in range(4):
            letters = random.choices(string.ascii_uppercase, k=2)
            digits = random.randint(100000, 999999)
            car_code = f"{''.join(letters)}{digits}"
            car_characters = string.ascii_letters
            car_name = ''.join(random.choice(car_characters) for _ in range(10))
            car_capacity = random.randint(2, 10)
            car_horsepower = random.randint(100, 400)
            car_weight = random.randint(200, 400)
            car_type = random.choice(["FWD", "RWD", "AWD"])
            Car(car_code, car_name, int(car_capacity), int(car_weight), int(car_horsepower), car_type)
            cars.append(f"{car_code}, {car_name}, {car_capacity}, {car_weight}, {car_horsepower}, {car_type}")
        retailer_info = (f"{retailer.retailer_id}, {retailer.retailer_name}, {retailer.carretailer_address}, "
                         f"{retailer.carretailer_business_hours}")
        info_string = retailer_info + ", " + str(cars) + "\n"
        test_data.append(info_string)
    try:
        os.makedirs("../data/")
    except OSError:
        print("Directory already exists")
    # Write test data to "stock.txt"
    with open("../data/stock.txt", "w") as file:
        file.write("".join(test_data))
    file.close()


def main():
    generate_test_data()  # Generate test data on program start
    path = "../data/stock.txt"
    car_retailers = []
    with open(path, "r") as file:
        for line in file.readlines():
            retailer_info = line.split(", ")
            car_retailers.append(CarRetailer(int(retailer_info[0]), retailer_info[1], retailer_info[2] + ", " +
                                             retailer_info[3], retailer_info[4] + ", "+retailer_info[5]))
    file.close()
    for retailer in car_retailers:
        print(retailer.__str__())
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            # Functionality 3: Look for the nearest car retailer
            try:
                user_postcode = int(input("Enter your four digit postcode: "))
                while user_postcode not in range(1000,10000):
                    print("Invalid postcode entered, please try again")
                    user_postcode = int(input("Enter your four digit postcode: "))
                nearest_retailer = None
                nearest_distance = float('inf')

                for retailer in car_retailers:
                    postcode_difference = retailer.get_postcode_distance(user_postcode)
                    if postcode_difference < nearest_distance:
                        nearest_distance = postcode_difference
                        nearest_retailer = retailer

                if nearest_retailer:
                    print(f"The nearest car retailer is {nearest_retailer.retailer_name}")
                    print(f"Retailer Address: {nearest_retailer.carretailer_address}")
                    print(f"with a Distance of: {nearest_distance} postcode units")
                else:
                    print("No car retailer found.")
            except ValueError:
                print("Invalid postcode. Please enter a valid integer postcode.")

        elif choice == "2":
            # Functionality 4: Get car purchase advice
            print("Available Car Retailers:")
            for i, retailer in enumerate(car_retailers):
                print(f"{i + 1}, Retailer ID: {retailer.retailer_id}, Retailer Name: {retailer.retailer_name}")

            # Prompt the user to select a car retailer
            while True:
                try:
                    retailer_choice = int(input("Select a car retailer (1, 2, etc.): ")) - 1
                    selected_retailer = car_retailers[retailer_choice]
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Please select a valid car retailer.")
            try:
                print(f"\nSelected Car Retailer: {selected_retailer.retailer_name}")
                print(f"Retailer Address: {selected_retailer.carretailer_address}")
                # Sub-menu for car purchase advice
                while True:
                    print("\nCar Purchase Advice Menu:")
                    print("1. Recommend a car")
                    print("2. Get all cars in stock")
                    print("3. Get cars in stock by car types")
                    print("4. Get probationary licence permitted cars in stock")
                    print("5. Back to Main Menu")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == "1":
                        # Functionality 4a: Recommend a car
                        recommended_car = selected_retailer.car_recommendation()
                        print(f"Recommended car: {recommended_car}")

                    elif sub_choice == "2":
                        # Functionality 4bii: Get all cars in stock
                        all_cars = selected_retailer.get_all_stock()
                        print("All cars in stock:")
                        for car in all_cars:
                            print(car)

                    elif sub_choice == "3":
                        # Functionality 4: Get cars in stock by car types
                        car_types = input("Enter car types separated by space (e.g., FWD AWD): ").split(" ")

                        while True:
                            valid_cartypes = []
                            for type in car_types:
                                if type in ["FWD","RWD","AWD"]:
                                    valid_cartypes.append(True)
                                else:
                                    valid_cartypes.append(False)
                            if all(valid_cartypes):
                                break
                            else:
                                print("invalid cartype, please enter again")
                                car_types = input("Enter car types separated by space (e.g., FWD AWD): ").split(" ")
                        matching_cars = selected_retailer.get_stock_by_car_type(car_types)
                        if matching_cars:
                            print("Cars in Stock by Car Types:")
                            for car in matching_cars:
                                print(f"Car Code: {car.car_code}, Car Type: {car.get_car_type()}")
                        else:
                            print("No matching cars available in stock for the specified car types.")

                    elif sub_choice == "4":
                        # Functionality 4biv: Get probationary licence permitted cars in stock
                        licence_type = input("Enter your licence type (L for Learner, P for Probationary, "
                                             "Full for Full): ")
                        while licence_type not in ["P", "L", "Full"]:
                            print("Invalid Licence type..")
                            licence_type = input("Enter your licence type "
                                                 "(L for Learner, P for Probationary, Full for Full): ")
                        licence_type = licence_type.strip().upper()
                        matching_cars = selected_retailer.get_stock_by_licence_type(licence_type)
                        if matching_cars:
                            print(f"Permitted Cars for licence type {licence_type} in Stock is: ")
                            for car_code in matching_cars:
                                print(car_code)
                        else:
                            print("Not allowed for probationary licence permitted cars.")

                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid choice. Please select a valid option (1-5).")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "3":
            # Functionality 5: Place a car order
            print("Place a Car Order:")
            try:
                user_input = input("Enter Retailer ID and Car Code (separated by a space): ")
                retailer_id, car_code = user_input.split()
                # Find the selected retailer
                selected_retailer = None
                for retailer in car_retailers:
                    if retailer.retailer_id == int(retailer_id):
                        selected_retailer = retailer
                        if car_code in [cars.car_code for cars in retailer.retailer_stock]:
                            order = selected_retailer.create_order(car_code)
                            if order:
                                with open("../data/order.txt", "a") as order_file:
                                    order_file.write(str(order) + '\n')
                                print(f"Order placed successfully!")
                        else:
                            print("Car not available....")
                        break
                if selected_retailer is None:
                    print("Retailer not found.")
            except ValueError as e:
                print("Invalid input format. Please enter Retailer ID and Car Code separated by a space.", e)

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option (1-4).")


if __name__ == "__main__":
    main()
