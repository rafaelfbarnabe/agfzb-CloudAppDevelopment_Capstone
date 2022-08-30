from django.db import models
from django.utils.timezone import now
import datetime

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    brand_name = models.CharField(null=False, max_length=30)
    brand_description = models.CharField(max_length=500)
    
    def __str__(self):
        return "Brand: " + self.brand_name + ", " + \
            "Descripion: " + self.brand_description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField()
    CAR_TYPES = (("con", "Convertible"), ("htb", "Hatchback"), ("miv", "Minivan"), ("put", "Pickup Truck"), ("sed", "Sedan"), ("suv", "SUV"), ("wag", "Wagon"))
    car_type = models.CharField(max_length=3, choices=CAR_TYPES)
    # YEARS = []
    # for y in range(1922, (datetime.datetime.now().year+1)):
    #     YEARS.append((y,y))

    # year = models.IntegerField(max_length=4, choices=YEARS, default=datetime.datetime.now().year)
    year = models.DateField(null=True)
    CAR_COLORS = (("bei", "Beige"), ("bla", "Black"), ("blu", "Blue"), ("bro", "Brown"), ("gol", "Gold"), ("gra", "Gray"), ("gre", "Green"), ("ora", "Orange"), ("pur", "Purple"), ("red", "Red"), ("sil", "Silver"), ("whi", "White"), ("yel", "Yellow"))
    car_color = models.CharField(max_length=3, choices=CAR_COLORS)
    
    def __str__(self):
        return "Brand: " + str(self.car_make) + ", " + \
            "Model: " + self.model_name + ", " + \
            "Type: " + self.car_type + ", " + \
            "Color: " + self.car_color + ", " + \
            "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    
    def __init__(self, dealership, name, purchase, review, purchase_date="", car_make="", car_model="", car_year="", sentiment="", id=""):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealership: " + str(self.dealership) + \
            "Name: " + self.name + \
            "Purchase: " + str(self.purchase) + \
            "Review: " + self.review + \
            "Purchase Date: " + self.purchase_date + \
            "Car Maker: " + self.car_make + \
            "Car Model: " + self.car_model + \
            "Car Year: " + str(self.car_year) + \
            "Sentiment: " + self.sentiment + \
            "ID: " + str(self.id)
