'''

This script reads through the MTA turnstile data files and calculates the incremental counts 
for entries and exits. This needs to be done because the data files show a snapshot value for 
entries and exits, which keeps increasing over time, instead of the value for the current time period. 

The output is a set of files showing the key, date, time and the values.

Values for entries and exits are stored in a dictionalry to keep the values continuous between input files.
The dictionary stores the key (combination of C/A and SCP), and the values for ENTRIES and EXITS.

Incomplete records are identified and rejected during the processing.

'''

from pathlib import Path
import glob
import pandas as pd
from timeit import default_timer as timer
from displayduration import DisplayDuration


# initialize variables and record starting time
path = Path('<path/to/data/files>')
previous_ca, previous_scp = '', ''
previous_entries, previous_exits = 0, 0
latestvalues = dict()
starttime = timer()


# this function returns the values for the key if it exists, or (0,0) otherwise
def GetLatest(ca, scp):
	if (ca, scp) in latestvalues:
		return latestvalues[row['C/A'], row['SCP']]
	else:
		return (0, 0)


# get a list of files to process; the current file layout started on 10/18/2014
files = [f for f in glob.glob(path / 'turnstile_20*.txt') if f >= path / 'turnstile_20141018.txt']

# create the output file, set file size counters
outf = open(path / '_outf-01.txt', 'w')
rowcount = 0
filenum = 2

# iterate the files and process the rows
for file in files:

	print('Processing file ' + file[23:])
	
	# read the file in a dataframe
	infile = pd.read_csv(file)

	# clean up the column names (some names have trailing spaces)
	infile.rename(columns=lambda x: x.strip(), inplace=True)
	
	# go through the rows and calculate the entries/exits
	for index, row in infile.sort_values(['C/A', 'UNIT', 'SCP', 'DATE', 'TIME']).iterrows():
		
		# control the size of the output files by limiting the number of rows written in each file
		if rowcount >= 5000000:
			outf.close()
			filename = '_outf-' + str(filenum).zfill(2) + '.txt'
			outf = open(path / filename, 'w')
			rowcount = 0
			filenum += 1

		# identify changes in c/a or scp, and retrieve the corresponding values from past files
		if (previous_ca != '' and previous_ca != row['C/A']) or (previous_scp != '' and previous_scp != row['SCP']):
			# record values for previous ca+scp
			latestvalues[previous_ca, previous_scp] = (previous_entries, previous_exits)
			# retrieve values for current ca+scp
			previous_entries, previous_exits = GetLatest(row['C/A'], row['SCP'])
				
		# write the row to output file, skip if values are missing or cannot be calculated
		if previous_entries+previous_exits != 0 and not (row.isnull().values.any()):
			# ensure numbers are treated as integer; pandas reads some numbers in the files as string
			row['ENTRIES'] = int(pd.to_numeric(row['ENTRIES']))
			row['EXITS'] = int(pd.to_numeric(row['EXITS']))
			# write to file
			outf.writelines(str(row['C/A'])+', '+str(row['SCP'])+', '+str(row['DATE'])+', '+str(row['TIME'])+', '+str(row['ENTRIES'])+', '+str(row['EXITS'])+', '+str(row['ENTRIES']-int(previous_entries))+', '+str(row['EXITS']-int(previous_exits))+'\n')
			rowcount += 1

		# set values for next iteration; set 0 if values are missing
		previous_ca = row['C/A']
		previous_scp = row['SCP']
		previous_entries = 0 if pd.isnull(row['ENTRIES']) else row['ENTRIES']
		previous_exits = 0 if pd.isnull(row['EXITS']) else row['EXITS']


# close output file, record end time, display duration
outf.close()
endtime = timer()
DisplayDuration(starttime, endtime)
