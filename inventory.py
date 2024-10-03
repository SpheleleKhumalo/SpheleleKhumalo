class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        # Initialize attributes
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        # String representation of a shoe object
        return f"{self.product} ({self.code}): {self.quantity} available at R{self.cost:.2f}"
    

shoe_list = []


def read_shoes_data(inventory_txt_file):
    # Read shoe data from inventory file
    try:
        with open(inventory_txt_file, "r") as inventory_file:
            next(inventory_file) # Skip the header line
            for line in inventory_file:
                shoe_data = line.strip().split(",")
                country, code, product, cost, quantity = shoe_data
                shoe_list.append(Shoe(country, code, product, float(cost), int(quantity)))
    except FileNotFoundError:
        print("Error: File not found.")


def capture_shoes():
    # Capture user input to create a new shoe
    country = input("Please enter country: ")
    code = input("Please enter code: ")
    product = input("Please enter product name: ")
    cost = float(input("Please enter cost: "))
    quantity = int(input("Please enter quantity: "))
    shoe_list.append(Shoe(country, code, product, cost, quantity))


def view_all():
    # print details of all shoes
    for shoe in shoe_list:
        print(shoe)


def re_stock():
    # Find the shoe with the lowest quantity and restock
    lowest_qty_shoe = min(shoe_list, key=lambda x: x.quantity)
    print(f"Lowest quantity shoe: {lowest_qty_shoe}")
    add_shoe_qty = int(input("Enter additional quantity to restock: "))
    lowest_qty_shoe.quantity += add_shoe_qty


def search_shoe(code):
    # Search for a shoe by code
    for shoe in shoe_list:
        if shoe.code == code:
            return shoe
    return None


def value_per_item():
    # Calculate and print total value for each shoe
    for shoe in shoe_list:
        total_value = shoe.cost * shoe.quantity
        print(f"{shoe.product}: Total value = R{total_value:.2f}")


def highest_qty():
    # Find the shoe with the highest quantity
    highest_qty_shoe = max(shoe_list, key=lambda x: x.quantity)
    print(f"Highest quantity shoe: {highest_qty_shoe}")


# Read data from file
read_shoes_data("inventory.txt")

while True:
    # Provide menu for a use to choose from.
    print("\nMenu")
    print("1. Add new shoe")
    print("2. View all shoes")
    print("3. Restock")
    print("4. Search by code")
    print("5. Calculate value per item")
    print("6. Find Highest quantity product")
    print("7. Exit")
    user_choice = input("Enter your choice from the menu: ")

    # Perform action based on user choice
    if user_choice == "1":
        capture_shoes()
    elif user_choice == "2":
        view_all()
    elif user_choice == "3":
        re_stock()
    elif user_choice == "4":
        code_to_search = input("Enter shoe code to search: ")
        shoe_found = search_shoe(code_to_search)
        if shoe_found:
            print(f"This is the shou you are looking for: {shoe_found}")
        else:
            print("Shoe not found.")
    elif user_choice == "5":
        value_per_item()
    elif user_choice == "6":
        highest_qty()
    elif user_choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please choose from the provided menu.")
