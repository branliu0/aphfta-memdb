#!/usr/bin/env ruby

require 'json'
require 'csv'
require 'pp'

FACILITIES_JSON = "../../fixtures/2013-01-16_facilities_with_zones.json"
ANDREW_CSV = "andrew_facilities.csv"
JSON_OUT = "andrew_out.json"

facilities = JSON.parse(File.read(FACILITIES_JSON))
andrew = CSV.read(ANDREW_CSV)

puts "#{facilities.length} facilities"
puts "#{andrew.length} Andrew facilities"

# Normalize them
facilities.map! do |f|
  f["fields"]
end

andrew.map! do |f|
  f.map! { |x| x && x.strip }
  {
    "facility_name" => f[1],
    "address" => f[2],
    "location" => f[3],
    "contact" => f[4],
    "doctor_ic" => f[5],
    "qualifications" => f[6]
  }
end

# Now let's go through each facility...
facilities.each do |fac|
  # Is there a corresponding facility in andrew?
  f = andrew.find { |f| f["facility_name"] == fac["facility_name"] }
  # puts "#{fac["facility_name"]}: #{f ? "FOUND" : "NOT"}"

  # For now, let's just take care of the ones where we have a perfect match.
  # We'll take care of other matches if it's worth the investment
  next unless f

  # Always copy over the address
  fac["address"] = f["address"] unless f["address"].nil?

  # pp fac
  # pp f
end

# Convert facilities back to Django fixture format
facilities.map!.with_index do |f, i|
  {
    "pk" => 100 + i,
    "model" => "memdb.facility",
    "fields" => f
  }
end

File.open(JSON_OUT, "w") do |f|
  f.puts(JSON.pretty_generate facilities)
end
