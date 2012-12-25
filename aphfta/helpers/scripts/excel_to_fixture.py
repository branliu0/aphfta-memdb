import csv
import json

#	Facility Name	
# Facility Owner
# Telephone Number
#	Email	
# Region
# District / Location	
# Type
# Membership


def run():
  facilities = []
  csvfile = open("aphfta_facilites.csv", "rU")
  reader = csv.reader(csvfile)
  for row in reader:
    fields = {}
    
    fields["name"] = row[0]
    fields["owner"] = row[1]
    
    phone = row[2].replace(" ", "")
    phone = row[2].replace("/", ",")
    phone = phone.split(",")
    for i in range(len(phone)):
      if i == 0:
        fields["phone"] = phone[i]
      else:
        fields["phone{0}".format(i+1)] = phone[i]
    
    email = row[3].replace(" ", "")
    email = email.split(",")
    for i in range(len(email)):
      if i == 0:
        fields["email"] = email[i]
      else:
        fields["email{0}".format(i+1)] = email[i]
    
    fields["region"] = row[4]
    fields["district"] = row[5]
    fields["type"] = row[6]
    
    membership = row[7].lower()
    fields["membership"] = (membership != "no")
    
    facilities.append({"model": "memdb.facility", "fields": fields})
  
  outfile = open("2012_aphfta_facilities_final.json", "w")
  outfile.write(json.dumps(facilities))

if __name__ == "__main__":
  run()