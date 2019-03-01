# The DisplayDuration function is used to correctly display the completion
# time of a function or program in hours, minutes and seconds, including
# the correct spelling of 'hour(s)', 'minute(s)' and 'second(s)'.
# The output is "Completed in xx hour xx minutes xx seconds."
def DisplayDuration(starttime, endtime):

	m, s = divmod(int(endtime - starttime), 60)
	h, m = divmod(m, 60)

	duration = 'Completed in '

	if h > 0:
		if h > 1:
			duration = duration + str(h) + ' hours '
		else:
			duration = duration + str(h) + ' hour '
	if m > 0:
		if m > 1:
			duration = duration + str(m) + ' minutes '
		else:
			duration = duration + str(m) + ' minute '
	if s > 0:
		if s > 1:
			duration = duration + str(s) + ' seconds.'
		else:
			duration = duration + str(s) + ' second.'
	
	print(duration)
