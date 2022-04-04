import requests  # requests module allows to send HTTP request.
import csv
from bs4 import BeautifulSoup
import mysql.connector as mysql

req = requests.get(
    "https://www.flipkart.com/search?q=mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&as-pos=1&as-type=RECENT&suggestionId=mobiles%7CMobiles&requestId=d880cadf-96c3-472d-b134-4fc05ac82697&as-backfill=on")
soup = BeautifulSoup(req.content, "html.parser")
# print(soup.prettify())

res = soup.head  # retrieving the contents of head tag.
print(res.text)  # extract the title of page
# Mobiles- Buy Products Online at Best Price in India - All Categories | Flipkart.com

all_products = []   # create an empty list

products = soup.findAll("div", {"class": "_3pLy-c row"})
#print(products)

mydb = mysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="flipkartdb"
)

mycursor = mydb.cursor()

# for looping to get the contents and put in files
for product in products:
    # to extract the mobile names using .select
    mname = product.select("div > div._4rR01T")[0].text.strip()
    # select DOM elements with BeautifulSoup select methods
    # .select returns a Python list of all the elements, the first element with the [0] index.
    # strip method to remove extra newlines/whitespaces.
    print(mname)    # REDMI 10 (Midnight Black, 128 GB)
    # to extract the price using .select
    mprice = product.select("div > div._30jeq3")[0].text.strip()
    x = mprice.split("₹")
    print(x[1])
    print(mprice)   # ₹12,999

    sql = "INSERT INTO products (Mobile_Name, Price) VALUES (%s, %s)"
    val = (mname, x[1])
    mycursor.execute(sql, val)
    mydb.commit()

    all_products.append({
        "Name": mname,
        "Price": mprice
    })
print("Record Inserted Successfully...")
mydb.close()

print(all_products)

keys = all_products[0].keys()   # extract the keys from dictionary
print(keys)  # dict_keys(['Name', 'Price'])

# Generating CSV from data
with open('flipkart.csv', 'w', newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)

# Database

# mycursor.execute("CREATE TABLE products(Mobile_Name varchar(255), Price varchar(20))")
