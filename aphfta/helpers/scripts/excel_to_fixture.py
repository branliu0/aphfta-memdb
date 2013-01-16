#!/usr/bin/env python

import csv
import json

# 0. Facility Name
# 1. Facility Owner
# 2. Telephone Number
# 3. Email
# 4. Region
# 5. District / Location
# 6. Type
# 7. Membership
# 8. Zone


def run():
  facilities = []
  csvfile = open("aphfta_facilites.csv", "rU")
  reader = csv.reader(csvfile)

  pk = 100

  for row in reader:
    fields = {}
    fields["date_joined"] = "2012-01-20"

    fields["facility_name"] = row[0]
    fields["doctor_ic"] = row[1]

    phone = row[2].replace(" ", "")
    phone = row[2].replace("/", ",")
    phone = phone.split(",")
    for i in range(len(phone)):
      if i == 0:
        fields["tel_office"] = phone[i]
      else:
        fields["tel_office{0}".format(i+1)] = phone[i]

    email = row[3].replace(" ", "")
    email = email.split(",")
    for i in range(len(email)):
      if i == 0:
        fields["email"] = email[i]
      else:
        fields["email{0}".format(i+1)] = email[i]

    fields["region"] = row[4]
    fields["district"] = row[5]
    fields["membership_type"] = row[6]

    membership = row[7].lower()
    fields["membership"] = (membership != "no")

    fields["zone"] = row[8]

    facilities.append({"pk": pk, "model": "memdb.facility", "fields": fields})
    pk += 1

  outfile = open("2013-01-16_facilities_with_zones.json", "w")
  outfile.write(json.dumps(facilities, indent=2))

if __name__ == "__main__":
  run()
