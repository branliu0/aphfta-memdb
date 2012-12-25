import csv
import json

#	Facility Name	
# Facility Owner
# Telephone Number
#	Email	
# Region
# District / Location	
# Type


def run():
  facilities = []
  csvfile = open("aphfta_facilites.csv", "rU")
  reader = csv.reader(csvfile)
  for row in reader:
    facility = {}
    
    facility["name"] = row[0]
    facility["owner"] = row[1]
    
    phone = row[2].replace(" ", "")
    phone = row[2].replace("/", ",")
    phone = phone.split(",")
    for i in range(len(phone)):
      if i == 0:
        facility["phone"] = phone[i]
      else:
        facility["phone{0}".format(i+1)] = phone[i]
    
    email = row[3].replace(" ", "")
    email = email.split(",")
    for i in range(len(email)):
      if i == 0:
        facility["email"] = email[i]
      else:
        facility["email{0}".format(i+1)] = email[i]
    
    facility["region"] = row[4]
    facility["district"] = row[5]
    facility["type"] = row[6]
    
    facilities.append(facility)
  
  outfile = open("2012_aphfta_facilities_final.json", "w")
  outfile.write(json.dumps(facilities))

if __name__ == "__main__":
  run()