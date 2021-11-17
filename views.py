from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from .models import *

import requests, json, openpyxl as pe, time
from datetime import datetime, timedelta

# Create your views here.
# welcome page
def welcome(request):
	context = { 'articles': Article.objects.all(), 'last_apicall': APICall.objects.first(), 'article_count': Article.objects.count(), }
	return render(request, 'lhla/news-table.html', context)

# make gnews API calls
def gnews_api():
	# using the gnews api
	url = "https://gnews.io/api/v4/search"
	token = "add_token_here"

	# date parameters… last 90 days -- try march 2020 - ...
	# 2021-10-31T18:57:19Z
	dt_from = "%sT18:57:19Z" % (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
	# dt_from = (datetime.now() - timedelta(days=90)).isoformat()

	# search terms
	places = [ 'Long Beach', 'Los Angeles', 'Santa Clarita', 'Glendale', 'Lancaster', 'LA', 'Palmdale', 'Torrance', 'Pasadena', 'Downey', 'San Gabriel', 'San Fernando', 'Santa Clara', 'Burbank', 'Inglewood', 'San Pedro', 'West Covina', 'El Monte', 'Norwalk', 'Artesia', 'San Fernando', 'Van Nuys', 'Hollywood', 'San Bernardino', 'Ventura', 'Orange', 'San Diego', 'Riverside' ]
	
	terms = [ 'hate crime', 'racial profiling', 'anti asian', 'anti semitism', 'anti gay', 'anti lgbt', 'white supremist', 'harassment', 'vandalism', 'graffiti', 'assault', 'threat', 'intimidation', 'asian crime', 'aapi hate', ]

	search_terms = []
	for i in terms:
		for k in places:
			search_terms += [ "%s %s" % (i, k, ) ]

	filename = '/var/www/html/files/lhla/gnews-results.xlsx'

	# open the workbook
	wb = pe.load_workbook(filename)

	# open the api sheet and get max row for api_id
	api_sheet = wb['API Calls']

	# open the articles sheet
	articles_sheet = wb['Articles']

	# make the calls and build xlsx -- sheet for individual articles and sheet for API calls
	params = { "token": token, "country": "us", "lang": "en", }
	header = []
	rows = []
	search_terms.reverse()
	for i, s in enumerate(search_terms[99:]):
		try:
			params["q"] = s
			params["from"] = dt_from
			req = requests.get(url, params=params)
			r = json.loads(req.content.decode('utf-8'))

			# make the API Calls row
			# insert to db
			apicall = APICall(search_term=s, total_articles=r['totalArticles'])
			apicall.save()
			row_api = [ apicall.search_term,  apicall.total_articles, str(apicall.dt_add), apicall.id ]
			api_sheet.append(row_api)
			
			# make the article rows
			for a in r['articles']:
				# check if in db already, based on url
				article = Article.objects.filter(url=a['url'])
				if len(article):
					continue

				article = Article(apicall=apicall, title=a['title'], description=a['description'], content=a['content'], url=a['url'], image=a['image'], published_at=a['publishedAt'], source_name=a['source']['name'], source_url=a['source']['url'])
				article.save()
				row_article = [ article.apicall.search_term, article.title, article.description, article.content, article.url, article.image, article.published_at, article.source_name, article.source_url, article.apicall.id ]
				articles_sheet.append(row_article)

			print (i, s, r['totalArticles'])
		except Exception as e:
			print ("Error,", s, e, req.url)
			break

		time.sleep(2)
		
	wb.save(filename)