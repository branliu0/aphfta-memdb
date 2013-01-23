#!/usr/bin/env ruby

require 'json'
require 'csv'
require 'pp'

PROGRAMS_CSV = 'programs.csv'
FACILITIES_JSON = 'programs.json'

programs_csv = CSV.read(PROGRAMS_CSV)
facilities = JSON.parse(File.read(FACILITIES_JSON))

# Add descriptive fields to the programs
programs = programs_csv.map do |p|
  p.map! { |x| x && x.strip }
  {
    :name => p[0],
    :doctor_ic => p[1],
    :address => p[2],
    :email => p[3],
    :phone => p[4],
    :location => p[5],
    :program => p[7].to_i,
    :facility_id => p[8] && p[8].to_i
  }
end

programs.each.with_index do |p, i|
  unless p[:facility_id]
    # Find the corresponding facility
    name = p[:name]
    fs = facilities.select do |f|
      f["fields"]["facility_name"].gsub(/\W/, '').downcase == name.gsub(/\W/, '').downcase
    end

    if fs.empty?
      puts "No matches for #{name}"
      print "Please enter the facility id: "
      id = gets.chomp.to_i
    elsif fs.length > 1
      puts "Multiple matches: " + (fs.map { |f| f["fields"]["facility_name"] }.join ",")
    else
      id = fs[0]["pk"]
    end
    p[:facility_id] = id
    programs_csv[i][8] = id
  end
end

CSV.open(PROGRAMS_CSV, "wb") do |csv|
  programs_csv.each do |row|
    csv << row
  end
end
