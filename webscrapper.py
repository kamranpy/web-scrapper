import urllib.request
import re
import csv

#Fetching Links
def horses(page):
  hrefList = []
  url = "https://www.olx.pt/d/animais/cavalos/?page=" + page

  file = urllib.request.urlopen(url)

  # Finding Links
  for line in file:
    decoded_line = line.decode("utf-8")

    if not ("data-emotion-css") in decoded_line:
      continue

    results = [i for i in range(len(decoded_line)) if decoded_line.startswith("/d/anuncio", i)]

    for result in results:
      hrefIndex = decoded_line[result:result+100]

      href_start = hrefIndex.find("/")
      href_end = hrefIndex.find(".html")

      hrefList.append(hrefIndex[href_start:href_end+5])

  return(hrefList)

links = []
for i in range(1, 14):
  res = horses(str(i))
  links.append(res)

flatLinks = [x for sublist in links for x in sublist]

# Fetching Products
final_result = []

for num, url_prod in enumerate(flatLinks):
  url_prod_comb = "https://www.olx.pt" + url_prod
  file_prod = urllib.request.urlopen(url_prod_comb)
  print("Record Fetched", num, "out of", len(flatLinks))

  desc_list = []
  for line in file_prod:
    decoded_line = line.decode("utf-8")

    # Finding Date
    date_index = decoded_line.find("Member Since")
    if(date_index > 0):
      raw_date = decoded_line[date_index:date_index+50]
      date_index_start = raw_date.find("Since")
      date_index_end = raw_date.find("<")
      date = raw_date[date_index_start+5:date_index_end]

    # Finding Image
    img_index = decoded_line.find("og:image")

    if(img_index > 0):
      raw_image = decoded_line[img_index:img_index+150]
      image_index_start = raw_image.find("=")
      image_index_end = raw_image.find(";")
      image = raw_image[image_index_start+2:image_index_end]

    # Finding Price
    price_index = decoded_line.find("displayValue")

    if(price_index > 0):
      raw_price = decoded_line[price_index:price_index+50]
      price_index_start = raw_price.find(":")
      price_index_end = raw_price.find("€")
      price = raw_price[price_index_start+3:price_index_end+1]

    
    # Finding Location
    city_index = decoded_line.find("cityNormalizedName")

    if(city_index > 0):
      raw_city = decoded_line[city_index:city_index+50]
      city_index_start = raw_city.find(":")
      city_index_end = raw_city.find(",")
      city = raw_city[city_index_start+3:city_index_end-2] 

    # Finding Description
    desc_index = decoded_line.find("<br />")

    if(desc_index > 0):
      raw_desc = decoded_line[desc_index-200:desc_index]
      desc_list.append(raw_desc)

  if desc_list:
    desc_list.pop(0)

  final_result.extend([[num, url_prod_comb, date, image, price, city, desc_list]])


# Writing to CSV File
with open('results1.csv', 'w', newline='', encoding='utf-8') as f:
  writer = csv.writer(f)
  writer.writerow(['Listing Number', 'Product Link', 'Date', 'Image Link', 'Price', 'Location', 'Description'])
  writer.writerows(final_result)
