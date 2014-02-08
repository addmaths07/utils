import glob
import os
import datetime
import sys

CSV_HEADERS = ['Subject', 'Start Date', 'Start Time',
		'End Date', 'End Time', 'All Day Event',
		'Description', 'Location', 'Private']

ICS_HEADERS = ['BEGIN', 'PRODID', 'VERSION',
	'ORGANIZER', 'SUMMARY', 'DESCRIPTION',
	'LOCATION', 'DTSTART', 'DTEND', 'DTSTAMP']
def getICSObject(f):

	icsObject = {}
	previousKey = ''
	for line in f.readlines():
		print line
		try:
			line  = line.strip()
			item = line.split(':')
			icsObject[item[0]] = item[1]
			previousKey = item[0]
		except IndexError, e:
			icsObject[previousKey] = icsObject[previousKey] + ' ' + item[0]
	return icsObject

def getDateValue(date_string):
	date_string = date_string[:8]
	format1 = "%Y%m%d"
	format2 = "%d/%m/%Y"
	return datetime.datetime.strptime(date_string, format1).strftime(format2)




def getCSVContent(src_dir):

	os.chdir(src_dir)
	csvList = []

	for icsFile in glob.glob("*.ics"):
		csvContent = {}
		f = open(icsFile,'r')
		# handle the mapping here as one wants
		icsObject = getICSObject(f)
		csvContent['Subject'] = '"'+icsObject['SUMMARY']+'"'
		csvContent['Start Date'] = getDateValue(icsObject['DTSTART'])
		csvContent['Start Time'] = '09:00:00 AM'
		csvContent['End Date'] = getDateValue(icsObject['DTEND'])
		csvContent['End Time'] = ''
		csvContent['All Day Event'] = ''
		csvContent['Description'] = '"'+icsObject['SUMMARY']+'"'
		csvContent['Location'] = '"City, Country"'
		csvContent['Private'] = ''
		csvList.append(csvContent)
		f.close()

	return csvList

def getCSVHeaderRow(data):
	headerStr = ''
	for item in data:
		headerStr = headerStr + item +','
	return headerStr[:len(headerStr)-1]

def getCSVDataRow(data):
	row = ''
	for key in CSV_HEADERS:
		row = row + data[key] +','
	return row[:len(row)-1]

def writeCSVList(csvList):
	f = open('abc.csv', 'w')
	f.write(getCSVHeaderRow(CSV_HEADERS))
	f.write('\n')
	for csvObject in csvList:
		#print csvObject
		f.write(getCSVDataRow(csvObject))
		f.write('\n')
	f.close()

def main(argv):
	try:
		src_dir = argv[0]
		dest_file_name = argv[1]
	except Exception, e:
		print "Please use Correct command i.e ics_csv_convertor.py <source Dir> <destination filename>"
		src_dir = "<source-dir-path>"
		dest_file_name = 'abc.csv'
	
	try:
		csvList = getCSVContent(src_dir)
		writeCSVList(csvList)
		f = open(dest_file_name, 'r')
		print f.read()
		f.close()
	except:
		print "Failed with default input"


if __name__ == "__main__":
	main(sys.argv[1:])
