import requests
from bs4 import BeautifulSoup
from colorama import Fore

kaufland_url = "https://glovoapp.com/bg/bg/sofiya/kaufland-sof/"
fantastiko_url = "https://glovoapp.com/bg/bg/sofiya/fantastiko-sof/"
# Getting the Html for both supermarkets
kaufland_result = requests.get(kaufland_url)
kaufland_result_after_request = BeautifulSoup(kaufland_result.text, "html.parser")

fantastiko_result = requests.get(fantastiko_url)
fantastiko_result_after_request = BeautifulSoup(fantastiko_result.text, "html.parser")

# Getting the store ratings
# The HTML is surrounded by blank spaces, so I use strip to remove them. You can also use comprehension
kaufland_rating = kaufland_result_after_request.find('span', "store-rating__label")
kaufland_rating_processed = "".join([x.strip() for x in kaufland_rating.string])
# kaufland_rating_processed = "".join([x for x in kaufland_rating.string if x != " " and x != "\n"])

fantastiko_rating = fantastiko_result_after_request.find('span', "store-rating__label")
fantastiko_rating_processed = "".join([x.strip() for x in fantastiko_rating.string])
# fantastiko_rating_processed = "".join([x for x in fantastiko_rating.string if x != " " and x != "\n"])

print(
    f"Welcome to Glovo!!!\nKaufland's current rating is {kaufland_rating_processed}\nFantastiko's current rating is {fantastiko_rating_processed}\nInput {Fore.BLUE}1{Fore.RESET} for Kaufland or {Fore.BLUE}2 {Fore.RESET}for Fantastiko.")

number = input("Type Here: ")
while True:
    if number != "1" and number != "2":
        print(f"{Fore.RED}Incorrect option{Fore.RESET} Try again")
        number = input("Type Here: ")
        continue
    if number == "1":
        chosen_link = "https://glovoapp.com/bg/bg/sofiya/kaufland-sof/?content=nay-prodavani-ts"
        break
    chosen_link = "https://glovoapp.com/bg/bg/sofiya/fantastiko-sof/?content=nay-prodavani-ts"
    break


class GettingInformation:

    def __init__(self, link):
        self.link = link
        self.request = requests.get(self.link)
        self.result = BeautifulSoup(self.request.text, "html.parser")

    def get_prices(self):
        # Another idea working for prices less than 10 leva
        # for price in prices:
        #     all_prices.append(price.string)
        # for price in prices:
        #     price_as_string = price.string
        #     filtered_word = ""
        #     flag = False
        #     for letter in price_as_string:
        #         if letter.isdigit() or letter == ",":
        #             if len(filtered_word) == 4:
        #                 flag = True
        #                 break
        #             filtered_word += letter
        #     if flag:
        #         break
        #     filtered_word += " лв"
        #     all_prices.append(filtered_word)
        prices = self.result.find_all('span', "product-price__effective product-price__effective--new-card")
        all_prices = []
        for price in prices:
            price_as_string = price.string
            filtered_word = price_as_string[5:-7]
            filtered_word += " лв"
            all_prices.append(filtered_word)
        return all_prices

    def get_names(self):
        names = self.result.find_all('span', weight="book")
        all_names = []
        for name in names:
            name_as_string = name.string
            filtered_word = name_as_string[7:-16]
            all_names.append(filtered_word)
        return all_names


obj = GettingInformation(chosen_link)
first_lst = obj.get_names()
second_lst = obj.get_prices()

# Creating a dictionary with the products as keys and prices as values
my_dictionary = dict(zip(first_lst, second_lst))

print("\n".join([f"{key} - {Fore.BLUE}{value}{Fore.RESET}" for key, value in my_dictionary.items()]))
