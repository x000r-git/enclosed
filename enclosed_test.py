import unittest
from urllib.request import urlopen
from modules.port_scan import run_port_scan
from modules.whois_results import filter_response
from modules.leakcheck_results import parse_output
from modules.domain_enum import information_from_crtsh
from modules.generate_output_format import create_header
from enclosed import create_output_file, load_configuration

### From https://www.tutorialspoint.com/How-do-I-create-a-Python-namespace
class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
###

class EnclosedTest(unittest.TestCase):
    def test_port_scan(self):
        self.assertEqual(run_port_scan(Namespace(domain="scanme.nmap.org", ip="45.33.32.156")), [22, 80])

    def test_file_creation(self):
        self.assertEqual(create_output_file(Namespace(domain='test.com')), "test.com.result")

    def test_configuration_import(self):
        self.assertEqual(load_configuration(), [['domain_enum', 'port_scan', 'leakcheck_results', 'whois_results'], ['domain_enum', 'leakcheck_results', 'whois_results']])

    def test_extracting_from_crtsh(self):
        self.assertEqual(information_from_crtsh(Namespace(domain="apteka.ru")), ['analytics.apteka.ru', 'api.apteka.ru', 'images.apteka.ru', 'importer.apteka.ru', 'old.apteka.ru', 'reports.apteka.ru', 'sitemaps.apteka.ru', 'staging.apteka.ru', 'static.apteka.ru', 'uploads.apteka.ru'])
        self.assertEqual(information_from_crtsh(Namespace(domain="auto.ru")), ['api2.auto.ru', 'auth.auto.ru', 'kiks.auto.ru', 'sso.auto.ru', 'testblog.auto.ru'])

    def test_parsing_leakcheck_output(self):
        self.assertEqual(parse_output("""{"success":true,"found":22,"passwords":59,"sources":[{"name":"000webhost.com","date":"2015-03"},{"name":"Aptoide.com","date":"2020-04"},{"name":"Avito.ru","date":"2016-11"},{"name":"CDEK","date":""},{"name":"Canva.com","date":"2019-05"},{"name":"Cfire.mail.ru","date":"2016-08"},{"name":"Collection 1","date":"2019-01"},{"name":"Crimecraft.mayngames.com","date":"2021-01"},{"name":"Disqus.com","date":"2012-07"},{"name":"FBK\/SmartVote\/Free.navalny.com","date":"2020-11"},{"name":"Free.navalny.com","date":"2021-02"},{"name":"Hostinger","date":""},{"name":"MMORG.net","date":""},{"name":"Mpgh.net","date":"2015-10"},{"name":"Ogusers","date":"2020-04"},{"name":"Parapa.mail.ru","date":"2016-08"},{"name":"Sendpulse.com","date":"2016-01"},{"name":"Sprashivai.ru","date":"2015-05"},{"name":"Stealer Logs","date":""},{"name":"VK.com","date":"2012-01"},{"name":"lolzteam.net","date":"2019-02"},{"name":"vkmix.com","date":"2020-02"}]}""", "admin@admin.admin"), "\n22 results for admin@admin.admin:\n000webhost.com\nAptoide.com\nAvito.ru\nCDEK\nCanva.com\nCfire.mail.ru\nCollection 1\nCrimecraft.mayngames.com\nDisqus.com\nFBK/SmartVote/Free.navalny.com\nFree.navalny.com\nHostinger\nMMORG.net\nMpgh.net\nOgusers\nParapa.mail.ru\nSendpulse.com\nSprashivai.ru\nStealer Logs\nVK.com\nlolzteam.net\nvkmix.com\n")

    def test_filtering_output(self):
        self.assertEqual(filter_response(urlopen("http://api.whois.vu/?clean&q=")), "Got an error. Try to recheck your CLI arguments...")

    def test_header_generation(self):
        self.assertEqual(create_header(), "***************************************************\n* test_module                                     *\n* it doesn't do anything                          *\n* it needs three arguments: name, surname, weight *\n***************************************************\n")

if __name__ == '__main__':
    unittest.main()