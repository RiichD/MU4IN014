from requests import *
from json import *
import unittest

class TestAPIMethods(unittest.TestCase):
	server_ip = "127.0.0.1"
	server_port = 8080
	#Tests pour le fichier XML dblp_2020_2020.xml
	def test_publications1_id(self):
		"""
		Test de la route /publications/id
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/1")
		l = loads(r1.text)
		self.assertEqual(l, {"author": "Louise A. Dennis", "title": "Computational Goals, Values and Decision-Making.", "pages": "2487-2495", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "5", "ee": "https://doi.org/10.1007/s11948-020-00244-y", "url": "db/journals/see/see26.html#Dennis20"})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/10")
		l = loads(r1.text)
		self.assertEqual(l, {"author": "Geerten van de Kaa", "author0": "Jafar Rezaei 0001", "author1": "Behnam Taebi", "author2": "Ibo van de Poel", "author3": "Abhilash Kizhakenath", "title": "How to Weigh Values in Value Sensitive Design: A Best Worst Method Approach for the Case of Smart Metering.", "pages": "475-494", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "1", "ee": "https://doi.org/10.1007/s11948-019-00105-3", "ee0": "https://www.wikidata.org/entity/Q92959988", "url": "db/journals/see/see26.html#KaaRTPK20"})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/100")
		l = loads(r1.text)
		self.assertEqual(l, {"author": "Katharina Fuerholzer", "author0": "Maximilian Schochow", "author1": "Florian Steger", "title": "Good Scientific Practice: Developing a Curriculum for Medical Students in Germany.", "pages": "127-139", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "1", "ee": "https://doi.org/10.1007/s11948-018-0076-7", "ee0": "https://www.wikidata.org/entity/Q90859423", "url": "db/journals/see/see26.html#FuerholzerSS20"})
	
	def test_publications2(self):
		"""
		Test de la route /publications
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/publications?limit=5")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis", "title": "Computational Goals, Values and Decision-Making.", "pages": "2487-2495", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "5", "ee": "https://doi.org/10.1007/s11948-020-00244-y", "url": "db/journals/see/see26.html#Dennis20"}, {"author": "Indira Nair", "author0": "William M. Bulleit", "title": "Pragmatism and Care in Engineering Ethics.", "pages": "65-87", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "1", "ee": "https://doi.org/10.1007/s11948-018-0080-y", "ee0": "https://www.wikidata.org/entity/Q90930992", "url": "db/journals/see/see26.html#NairB20"}, {"author": "Petr Houdek", "title": "Fraud and Understanding the Moral Mind: Need for Implementation of Organizational Characteristics into Behavioral Ethics.", "pages": "691-707", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "2", "ee": "https://doi.org/10.1007/s11948-019-00117-z", "ee0": "https://www.wikidata.org/entity/Q92736437", "url": "db/journals/see/see26.html#Houdek20"}, {"author": "M. Reza Hosseini", "author0": "Igor Martek", "author1": "Saeed Banihashemi", "author2": "Albert P. C. Chan", "author3": "Amos Darko", "author4": "Mahdi Tahmasebi", "title": "Distinguishing Characteristics of Corruption Risks in Iranian Construction Projects: A Weighted Correlation Network Analysis.", "pages": "205-231", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "1", "ee": "https://doi.org/10.1007/s11948-019-00089-0", "ee0": "https://www.wikidata.org/entity/Q91374986", "url": "db/journals/see/see26.html#HosseiniMBCDT20"}, {"author": "Rafi Rashid", "title": "Training STEM Ph.D. Students to Deal with Moral Dilemmas.", "pages": "1861-1872", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "3", "ee": "https://doi.org/10.1007/s11948-019-00174-4", "ee0": "https://www.wikidata.org/entity/Q92485691", "url": "db/journals/see/see26.html#Rashid20"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/publications?limit=1")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis", "title": "Computational Goals, Values and Decision-Making.", "pages": "2487-2495", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "5", "ee": "https://doi.org/10.1007/s11948-020-00244-y", "url": "db/journals/see/see26.html#Dennis20"}]})
	
	def test_author_name(self):
		"""
		Test de la route /authors/<name>
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis")
		l = loads(r1.text)
		self.assertEqual(l, {"data": {"Publications": 2, "Coauteurs": 4}})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/d")
		l = loads(r1.text)
		self.assertEqual(l, {"data": {"Publications": 0, "Coauteurs": 0}})
	
	def test_auth_pub(self):
		"""
		Test de la route /authors/<name>/publications
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/publications")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis", "title": "Computational Goals, Values and Decision-Making.", "pages": "2487-2495", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "5", "ee": "https://doi.org/10.1007/s11948-020-00244-y", "url": "db/journals/see/see26.html#Dennis20"}, {"author": "Peter Stringer", "author0": "Rafael C. Cardoso", "author1": "Xiaowei Huang 0001", "author2": "Louise A. Dennis", "title": "Adaptable and Verifiable BDI Reasoning.", "booktitle": "AREA@ECAI", "year": "2020", "pages": "117-125", "crossref": "journals/corr/abs-2007-11260", "ee": "https://doi.org/10.4204/EPTCS.319.9", "ee0": "https://arxiv.org/abs/2007.11743", "url": "db/series/eptcs/eptcs319.html#abs-2007-11743"}, {"author": "Louise A. Dennis", "author0": "Michael Fisher 0001", "title": "Verifiable Self-Aware Agent-Based Autonomous Systems.", "pages": "1011-1026", "year": "2020", "volume": "108", "journal": "Proc. IEEE", "number": "7", "ee": "https://doi.org/10.1109/JPROC.2020.2991262", "url": "db/journals/pieee/pieee108.html#DennisF20"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/d/publications")
		l = loads(r1.text)
		self.assertEqual(l, {"data": []})
	
	def test_auth_coauthor(self):
		"""
		Test de la route /authors/<name>/coauthors
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/coauthors")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Peter Stringer"}, {"author": "Rafael C. Cardoso"}, {"author": "Xiaowei Huang 0001"}, {"author": "Michael Fisher 0001"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Peter Stringer/coauthors")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Rafael C. Cardoso"}, {"author": "Xiaowei Huang 0001"}, {"author": "Louise A. Dennis"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Peter Stringer/coauthors?start=1&count=2&order=author")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis"}, {"author": "Xiaowei Huang 0001"}]})
		
	def test_search_authors(self):
		"""
		Test de la route /search/authors/<searchString>
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Louise A. D")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Louise?start=1&count=5&order=author")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise Bezuidenhout"}, {"author": "Louise E. Tamindael"}, {"author": "Louise Leroux"}, {"author": "Louise Roberts"}, {"author": "Louise Willemen"}]})
	
	def test_search_pub(self):
		"""
		Test de la route /search/publications/<searchString>
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/Computational Goals")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Louise A. Dennis", "title": "Computational Goals, Values and Decision-Making.", "pages": "2487-2495", "year": "2020", "volume": "26", "journal": "Sci. Eng. Ethics", "number": "5", "ee": "https://doi.org/10.1007/s11948-020-00244-y", "url": "db/journals/see/see26.html#Dennis20"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/Computational Geometry?filter=author:im")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Joachim Gudmundsson", "author0": "Michiel H. M. Smid", "title": "Special issue on the 29th Canadian Conference on Computational Geometry, Guest Editors' foreword.", "pages": "101608", "year": "2020", "volume": "88", "journal": "Comput. Geom.", "ee": "https://doi.org/10.1016/j.comgeo.2020.101608", "url": "db/journals/comgeo/comgeo88.html#GudmundssonS20"}, {"author": "Athanasios Voulodimos", "author0": "Paraskevas Karagiannopoulos", "author1": "Ifigenia Drosouli", "author2": "Georgios Miaoulis", "title": "CGVis: A Visualization-Based Learning Platform for Computational Geometry Algorithms.", "pages": "288-302", "year": "2020", "booktitle": "EC-TEL", "ee": "https://doi.org/10.1007/978-3-030-57717-9_21", "crossref": "conf/ectel/2020", "url": "db/conf/ectel/ectel2020.html#VoulodimosKDM20"}]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/Computational Geometry?filter=author:im&order=author")
		l = loads(r1.text)
		self.assertEqual(l, {"data": [{"author": "Athanasios Voulodimos", "author0": "Paraskevas Karagiannopoulos", "author1": "Ifigenia Drosouli", "author2": "Georgios Miaoulis", "title": "CGVis: A Visualization-Based Learning Platform for Computational Geometry Algorithms.", "pages": "288-302", "year": "2020", "booktitle": "EC-TEL", "ee": "https://doi.org/10.1007/978-3-030-57717-9_21", "crossref": "conf/ectel/2020", "url": "db/conf/ectel/ectel2020.html#VoulodimosKDM20"}, {"author": "Joachim Gudmundsson", "author0": "Michiel H. M. Smid", "title": "Special issue on the 29th Canadian Conference on Computational Geometry, Guest Editors' foreword.", "pages": "101608", "year": "2020", "volume": "88", "journal": "Comput. Geom.", "ee": "https://doi.org/10.1016/j.comgeo.2020.101608", "url": "db/journals/comgeo/comgeo88.html#GudmundssonS20"}]})
		
	def test_authors_distance(self):
		"""
		Test de la route /authors/<name_origin>/distance/<name_destination>
		"""
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/M. Reza Hosseini/distance/Albert P. C. Chan")
		l = loads(r1.text)
		self.assertEqual(l, {"Distance": 3, "Path": ["M. Reza Hosseini", "Igor Martek", "Saeed Banihashemi", "Albert P. C. Chan"]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/distance/Peter Stringer")
		l = loads(r1.text)
		self.assertEqual(l, {"Distance": 3, "Path": ["Peter Stringer", "Rafael C. Cardoso", "Xiaowei Huang 0001", "Louise A. Dennis"]})
		r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/distance/Louise A. Dennis")
		l = loads(r1.text)
		self.assertEqual(l, {"Distance": 0, "Path": "SELF"})
if __name__ == '__main__':
	unittest.main()
