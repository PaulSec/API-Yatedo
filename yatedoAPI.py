"""
This is the (unofficial) Python API for Yatedo.com Website.
Using this code, you can manage to retrieve employees from a specific company

"""
import requests
from bs4 import BeautifulSoup
import re


class YatedoAPI(object):

    """
        YatedoAPI Main Handler
    """

    _instance = None
    _verbose = False

    def __init__(self, arg=None):
        pass

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(YatedoAPI, cls).__new__(
                cls, *args, **kwargs)
            if (args and args[0] and args[0]['verbose']):
                cls._verbose = True
        return cls._instance

    def display_message(self, s):
        if (self._verbose):
            print '[verbose] %s' % s

    def get_number_of_results(self, company_name):
        url = 'http://www.yatedo.com/s/companyname:(%s)/normal' % (company_name)
        self.display_message(url)
        req = requests.get(url)
        if 'did not match any' in req.content:
            return 0
        return re.search(r"<span id=\"snb_elm_m\">([\d\s]+)</span>", req.content).group(1).replace(' ', '')

    def search(self, company_name, start_index, page):
        url = 'http://www.yatedo.com/search/profil?c=normal&q=companyname:(%s)&rlg=en&uid=-1&start=%s&p=%s' % (company_name, start_index, page)
        self.display_message(url)
        req = requests.get(url)
        soup = BeautifulSoup(req.content)
        res = []
        for contact in soup.findAll('div', attrs={'class': 'span4 spanalpha ycardholder'}):
            contact_name = contact.find('a', attrs={})
            contact_job = contact.find('div', attrs={'class': 'ytdmgl'})
            contact_name = contact_name.text
            contact_job = contact_job.text[:-1]

            self.display_message("%s (%s)" % (contact_name, contact_job))
            # creating structure for the contact
            contact = {}
            contact['name'] = contact_name
            contact['job'] = contact_job
            res.append(contact)
        return res

    def get_employees(self, company_name):
        self.display_message('Fetching result for company "%s"' % (company_name))
        num = int(self.get_number_of_results(company_name))

        if num == 0:
            self.display_message('Stopping here, no results for %s' % company_name)
            return []

        res = {}
        res['company_name'] = company_name
        res['employees'] = []
        self.display_message('Found %s results, collecting them..' % (num))
        i = 0
        while i * 16 < num:
            new_employees = self.search(company_name, i * 16, i + 1)
            for employee in new_employees:
                res['employees'].append(employee)
            i = i + 1
        return res
        # return json.dumps(res)
