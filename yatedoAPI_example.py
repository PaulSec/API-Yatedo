from yatedoAPI import YatedoAPI

# verbose mode
res = YatedoAPI({'verbose': True}).get_employees('CompanyName')
print res  # retrieves the results

# non verbose mode
res = YatedoAPI().get_employees('CompanyName')
print res  # retrieves the results
