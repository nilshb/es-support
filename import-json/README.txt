Import CSV file to ES

uses matrikkel adresses from all of norway. The format must match:

gate = line[7]
nummer = line[8] + line[9]
postnr = line[19]
poststed = line[20].capitalize()

where line is an array containing a line from the csv file.
