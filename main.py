# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from google.appengine.api import urlfetch
import json

class WhoKnows(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		tech = self.request.get("text")
		parsedTech = '"' + tech.replace(" ", "%20") + '"'
		url = 'http://stack.ciandt.com/api/public/whoknows?q='+parsedTech+"&top=10"
		try:
			result = urlfetch.fetch(url)

			if result.status_code == 200:
				data = json.loads(result.content)
				if data:
					names = "These are the *top 10 dudes* that know '*"+ tech + "*':\n\n"
					for item in data:
						names += item["name"].title() + " (*" + item["login"] + "*)"+ " from "+ item["city"] + "\n"
					
					self.response.write(names)
				else:
					self.response.write("Sorry, nobody knows '*" + tech + "*'.")
			else:
				self.response.status_code = result.status_code
		except urlfetch.Error:
			logging.exception('Caught exception fetching url')

class WhichProjectUses(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		tech = self.request.get("text")
		parsedTech = '"' + tech.replace(" ", "%20") + '"'
		url = 'http://stack.ciandt.com/api/public/whichprojectuses?q='+parsedTech+"&top=10"
		try:
			result = urlfetch.fetch(url)

			if result.status_code == 200:
				data = json.loads(result.content)
				if data:
					projects = "These are the *top 10 project* that uses '*"+ tech + "*':\n\n"
					for item in data:
						projects += "*" + item["contract"].title() + " - " + item["flow"].title() + "*, has *" + item["technology"] + "* with total skill of *" + str(item["achieve"]) + "*\n"
					
					self.response.write(projects)
				else:
					self.response.write("Sorry, no project uses '*" + tech + "*'.")
			else:
				self.response.status_code = result.status_code
		except urlfetch.Error:
			logging.exception('Caught exception fetching url')


app = webapp2.WSGIApplication([
    ('/whoknows', WhoKnows),
    ('/whichprojectuses', WhichProjectUses)
], debug=True)
