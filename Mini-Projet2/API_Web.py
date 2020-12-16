from bottle import route, request, run, SimpleTemplate, template
from json import *
from requests import get

server_ip = "127.0.0.1"
server_port = 8080

@route("/input")
def input():
	return '''
	<form action="/input" method="post">
	Word: <input name="author_data" type="text" /> <br/>
	Start: <input name="start_data" type="text" /> <br/>
	Count: <input name="count_data" type="text" /> <br/>
	Order: <input name="order_data" type="text" /> <br/>
	filter: <input name="filter_data" type="text" /> <br/>
	<input name="f_publications" value="find publications" type="submit" />
	<input name="f_coauthors" value="find coauthors" type="submit" /> <br/>
	<input name="f_search_publications" value="search publications" type="submit" />
	</form>
	'''
	
@route("/input", method='POST')
def do_input():
	data = request.forms.getunicode("author_data")
	start = request.forms.getunicode("start_data")
	count = request.forms.getunicode("count_data")
	order = request.forms.getunicode("order_data")
	filter = request.forms.getunicode("filter_data")
	
	find_pub = request.forms.get('f_publications')
	find_co = request.forms.get('f_coauthors')
	find_search_pub = request.forms.get('f_search_publications')
	
	print(f"GET:{data}, buttons: find_pub:{find_pub}, find_co:{find_co}, find_search_pub:{find_search_pub}, start:{start}, count:{count}, order:{order}, filter:{filter}")
	r = ""
	l = "No data found"
	
	#Activation et vérification des options
	isStarting = False
	isCounting = False
	isOrdering = False
	isFiltering = False
	options = ''
	if start is not None and start != "":
		isStarting = True
		options += f"?start={start}"
	if count is not None and count != "":
		isCounting = True
		if isStarting:
			options += f"&count={count}"
		else:
			options += f"?count={count}"
	if order is not None and order != "":
		isFiltering = True
		if isStarting or isCounting:
			options += f"&order={order}"
		else:
			options += f"?order={order}"
	
	if find_pub:
		print(f"Checking publications for {data}\n")
		r = get(f"http://{server_ip}:{server_port}/authors/{data}/publications{options}")
	elif find_co:
		print(f"Checking coauthors for {data}\n")
		r = get(f"http://{server_ip}:{server_port}/authors/{data}/coauthors{options}")
	elif find_search_pub:
		if filter is not None and filter != "":
			isFiltering = True
			if isStarting or isCounting or isOrdering:
				options += f"&filter={filter}"
			else:
				options += f"?filter={filter}"
		print(f"Searching publications about {data}\n")
		r = get(f"http://{server_ip}:{server_port}/search/publications/{data}{options}")
	if r != '':
		l = loads(r.text)
	return l
run(host='localhost', port=8081)
