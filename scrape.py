import bs4
import requests
import csv

payload = {
	"user[email]": "<USER EMAIL>",
	"password[email]": "<PASSWORD>",
	# "csrf_token": "<CSRF_TOKEN>"
}

session_requests = requests.session()

login_url = 'https://angel.co/login'
result = session_requests.get(login_url)

tree = html.fromstring(result.text)


# https://kazuar.github.io/scraping-tutorial/

# foodtech = requests.get('https://angel.co/companies?keywords=foodtech')
#
# soup_food = bs4.BeautifulSoup(html, "html.parser")
#
# show_food = soup_food.select("div.base startup")
#
# food_info = [val.select(".company.column.g-lockup.text, .column.location.value, .column.website.value") for val in show_food]
#
# food_rows = [[val[0].text, val[1].text, val[2].text, 'foodtech']]
#
# with open('foodtech.tsv', 'a') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter=",")
#     if tsvfile.tell() == 0:
#         writer.writerow( ('Name', 'Location', 'Website'))
#     for row in food_rows:
#         writer.writerow( (row) )
