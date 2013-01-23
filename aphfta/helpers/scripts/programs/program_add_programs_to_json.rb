#!/usr/bin/env ruby

require 'json'
require 'csv'
require 'pp'

class NilClass
  def empty?; true; end
  def blank?; true; end
end

class String
  def blank?
    self.strip.length == 0
  end
end

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

programs.each do |p|
  next if p[:facility_id] == 0

  facility = facilities.find do |f|
    f["pk"] == p[:facility_id]
  end

  facility["fields"]["programs"] ||= []
  facility["fields"]["programs"] << p[:program]
  facility["fields"]["programs"].uniq!

  facility["fields"]["address"] = p[:address] if facility["fields"]["address"].blank?
  facility["fields"]["doctor_ic"] = p[:doctor_ic] if facility["fields"]["doctor_ic"].blank?

  unless p[:email].nil?
    if facility["fields"]["email"].blank?
      facility["fields"]["email"] = p[:email]
    elsif facility["fields"]["email"].downcase != p[:email].downcase
      if facility["fields"]["email2"].blank?
        facility["fields"]["email2"] = p[:email]
      elsif facility["fields"]["email2"].downcase != p[:email].downcase
        facility["fields"]["email3"] = p[:email]
      end
    end
  end

  unless p[:phone].nil?
    if facility["fields"]["tel_office"].blank?
      facility["fields"]["tel_office"] = p[:phone]
    elsif facility["fields"]["tel_office"].downcase != p[:phone].downcase
      if facility["fields"]["tel_office2"].blank?
        facility["fields"]["tel_office2"] = p[:phone]
      elsif facility["fields"]["tel_office2"].downcase != p[:phone].downcase
        facility["fields"]["tel_office3"] = p[:phone]
      end
    end
  end

  # pp p
  # pp facility["fields"]
  # gets
end

File.open(FACILITIES_JSON, "w") { |f| f.write(JSON.pretty_generate(facilities)) }
