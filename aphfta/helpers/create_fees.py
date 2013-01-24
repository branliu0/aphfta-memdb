from memdb.models import Facility, Fee
import json

infile = open("fixtures/2013-01-24_all_facilities.json", "r")

facilities = json.loads(infile.read())

for facility in facilities:
    f = Facility.objects.get(id=facility["pk"])
    for year, amount in facility["fees"].iteritems():
        if year == "registration":
            type = "registration"
            year = int(facility["registration_year"]) if facility["registration_year"] else 2013
        else:
            type = "annual"
            year = int(year)

        description = "imported from excel spreadsheet"
        fee = Fee(facility=[f], amount=int(amount), description=description, year=year, type=type)
        # fee.save()
