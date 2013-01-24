from memdb.models import Facility, Fee
import json
import csv

infile = open("fixtures/facility_payments_fixture_id.json", "r")

facilities = json.loads(infile.read())

outfile = open("fixtures/outstanding_facility_fees.csv", "w")
csvwriter = csv.writer(outfile)

# create_fees(facilities)

csvwriter.writerow([
    "Facility Name",
    "Address",
    "Location",
    "Contact",
    "Responsible",
    "Qualifications",
    "Registration",
    "Fee 2000",
    "Fee 2001",
    "Fee 2002",
    "Fee 2003",
    "Fee 2004",
    "Fee 2005",
    "Fee 2006",
    "Fee 2007",
    "Fee 2008",
    "Fee 2009",
    "Fee 2010",
    "Fee 2011",
    "Fee 2012",
    "Fee 2013",
    "Outstanding Balance",
    "Registration Year"
])


def create_fees(facilities):
    for facility in facilities:
        if facility["pk"] == 0:
            row = [
                facility["facility_name"],
                facility["address"],
                facility["location"],
                facility["contact"],
                facility["doctor_in_charge"],
                facility["qualifications"],
                facility["fees"]["registration"],
                facility["fees"]["2000"],
                facility["fees"]["2001"],
                facility["fees"]["2002"],
                facility["fees"]["2003"],
                facility["fees"]["2004"],
                facility["fees"]["2005"],
                facility["fees"]["2006"],
                facility["fees"]["2007"],
                facility["fees"]["2008"],
                facility["fees"]["2009"],
                facility["fees"]["2010"],
                facility["fees"]["2011"],
                facility["fees"]["2012"],
                facility["fees"]["2013"],
                facility["outstanding_balance"],
                facility["registration_year"]
            ]
            csvwriter.writerow(row)
            continue
        f = Facility.objects.get(id=facility["pk"])
        total = 0
        for year, amount in facility["fees"].iteritems():
            if not year or not amount: continue
            
            if year == "registration":
              t = "Registration"
              year = int(facility["registration_year"]) if facility["registration_year"] else 2013
            else:
              t = "Annual"
              year = int(year)
            description = "imported from excel spreadsheet"
            
            
            total += int(amount)
        
        # ob = int(facility["outstanding_balance"])
        # if not ob: continue
        # if total != ob:
        #     print "Facility: {0} | Total: {1}, Outstanding: {2}".format(facility["facility_name"], total, ob)
            
            fee = Fee(amount=int(amount), description=description, year=year, type=t)
            
            fee.save()
            
            fee.facility.add(f)
