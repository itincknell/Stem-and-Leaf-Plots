
import math

def print_stemplots(*plots):
	m = max([max([len(x) for x in plots[i]]) for i in range(len(plots))]) + 4 
	for i in range(min([len(plot) for plot in plots])):
		line = [plot[i] for plot in plots]
		for x in line:
			print(f"{x:<{m}}",end='')
		print()

def stem_negative_zero(scale, white_space, zero_fill):
	'''
	Handles correct padding when stem is a zero 
	and leaves are negative values
	'''
	if scale < .1:
		line = " " * (white_space - 2) + "-0." + "0" * (zero_fill - 1) + "|"
	elif scale == .1:
		line = " " * (white_space - 2) + "-0.|"
	else:
		line = " " * (white_space - 2) + "-0|" 
	return line

def stem_positive_zero(scale, white_space, zero_fill):
	'''
	Handles correct padding when stem is a zero 
	and leaves are positive values
	'''
	if scale < .1:
		line = " " * (white_space - 1) + "0." + "0" * (zero_fill - 1) + "|"
	elif scale == .1:
		line = " " * (white_space - 1) + "0.|"
	else:
		line = " " * (white_space - 1) +  "0|"
	return line

def stem_nonzero(scale, i, white_space, zero_fill):
	'''
	Handles correct padding when stem is non-zero
	'''
	if scale < .1:
		if i < 0:
			line = " " * (white_space - 2) + f"{round(i * 10 * scale, zero_fill):<0{zero_fill + 2}}|"
		else:
			line = " " * (white_space - 1) + f"{round(i * 10 * scale, zero_fill):<0{zero_fill + 1}}|"
	elif scale == .1:
		line = f"{i:>{white_space}}.|"
	else:
		line = f"{i:>{white_space}}|"
	return line

def leaf_negative_zero(dataset, stem_plot, scale, step, white_space, zero_fill):
	'''
	Handle case when stem is zero and leavs are negative.

	Generates a series of strings 'line' that start with 
	the stem value followed by leaf values.
	Appends the line to the return list stem as needed.
	'''

	# retreive properly formated stem
	line = stem_negative_zero(scale, white_space, zero_fill)

	# level controls when a change to a new line is needed
	# ex. if step = 2, two stems will appear; line is used
	# to calculate when to cut off the lower stem
	level = 1

	# iterate through entire data set to find negative leaves
	for j in dataset:

		# test for single-digit negative values
		if str(j)[0] == '-' and len(str(j)) == 2:

			# handle if current level exceeded, 
			# append line to stem_plot and create next stem 
			while (j % 10) >= (10 / step) * level:
				level += 1
				stem_plot.append(line)
				line = stem_negative_zero(scale, white_space, zero_fill)

			# append a single digit to line always
			line += str(j)[-1:]

	# append last 
	stem_plot.append(line)

	# each level of each stem must appear, even when empty
	while level != step:
		stem_plot.append(stem_negative_zero(scale, white_space, zero_fill))
		level += 1

	return stem_plot

def leaf_positive_zero(dataset, stem_plot, scale, step, white_space, zero_fill):
	'''
	Handle case when stem is zero and leavs are positive.

	Generates a series of strings 'line' that start with 
	the stem value followed by leaf values.
	Appends the line to the return list stem as needed.
	'''

	# retreive properly formatted stem
	line = stem_positive_zero(scale, white_space, zero_fill)

	# used when step is greater than 1 to create multiple stems
	level = 1

	# iterate through data set to find positive single digit values
	for j in dataset:

		# test if non-negative and single-digit
		if str(j)[0] != '-' and len(str(j)) == 1:

			# check if next level is needed, append previous level 
			# and generate new stem
			while (j % 10) >= (10 / step)*level:
				level += 1
				stem_plot.append(line)
				line = stem_positive_zero(scale, white_space, zero_fill)

			# append only a single digit
			line += str(j)[-1:]

	# append last line 
	stem_plot.append(line)

	# all levels must be used even if empty
	while level != step:
		stem_plot.append(stem_positive_zero(scale, white_space, zero_fill))
		level += 1

	return stem_plot

def leaf_nonzero(dataset, stem_plot, scale, step, i, white_space, zero_fill):
	'''
	Handle case when stem is non-zero.

	Generates a series of strings 'line' that start with 
	the stem value followed by leaf values.
	Appends the line to the return list stem as needed.

	'i' indicates the current stem to match leaves with

	'''

	# fetch first stem
	line = stem_nonzero(scale, i, white_space, zero_fill)

	# controls when step > 1, multiple levels per stem
	level = 1

	# iterate throught dataset and match values with 
	# current stem
	for j in dataset:

		# handle negative values
		if str(j)[0] == '-':

			# if all-but-last matches with 'i'
			if str(j)[:-1] == str(i):

				# check to see if next stem level is needed
				while (j % 10) >= (10 / step) * level:
					level += 1
					stem_plot.append(line)						
					line = stem_nonzero(scale, i, white_space, zero_fill)

				# append the last digit only
				line += str(j)[-1:]

		# handle positive values
		elif str(j)[0] != '-':

			# if all-but-last matches with 'i'
			if str(j)[:-1] == str(i):

				# check if next stem level is needed
				while (j % 10) >= (10 / step) * level:
					level += 1
					stem_plot.append(line)
					line = stem_nonzero(scale, i, white_space, zero_fill)

				# append the last digit only
				line += str(j)[-1:]

	# appead last line
	stem_plot.append(line)

	# all levels must be used even if empty
	while level != step:
		stem_plot.append(stem_nonzero(scale, i, white_space, zero_fill))
		level += 1

	return stem_plot


def stem_plot(dataset,scale,step=1,low=None,hi=None,label=None):
	'''
	Generates a stem and leaf plot based on a numeric list: dataset
	Returns the plot as a list with header information followed by rows
	
	scale determines the precision of leaves i.e. each leaf can represent 100, 1, .01
	
	step subdivides stems. Ex. set to 2, each stem with appear twice with values over 
	5 and values 4 and lower on different stems
	'''

	# Use custom label if provided, otherwise omit lable
	if label:
		stem_plot = [label,f"scale = {scale:,}"]
	else:
		stem_plot = [f"scale = {scale:,}"]

	# calculate leaf values by dividing by scale factor. Ex. if leaves 
	# represent .1, multiplies by 10 then rounds off zeros
	dataset.sort()
	for i in range(len(dataset)):
		dataset[i] = int(round(dataset[i]/scale,0))

	# determine the required padding based on min and max values
	min_value = min(dataset)
	max_value = max(dataset)

	# f value used to justify formated string
	if min_value <= -10 or max_value >= 100:
		f = 3
	elif min_value < 0 or max_value >= 10:
		f = 2
	else:
		f = 1

	# value used to justify stem with correct number of zeros
	zero_fill = int(-math.log10(scale))

	# determine the upper and lower bound if not set by hi and low
	low = int(min(dataset)//10) if low == None else low
	hi = int(max(dataset)//10)+1 if hi == None else hi

	# must iterate over entire range to avoid gaps
	for i in range(low,hi):

		# breaks down to three cases that are handled differently

		# first determine if stem is zero
		if i == 0:

			if low < 0:
				# if least stem value if negative
				stem_plot = leaf_negative_zero(dataset,stem_plot,scale,step,f, zero_fill)
			else:
				# if all stem values are positive
				stem_plot = leaf_positive_zero(dataset,stem_plot,scale,step,f, zero_fill)
		else:
			# all other cases where stem is non-zero
			stem_plot = leaf_nonzero(dataset,stem_plot,scale,step,i,f, zero_fill)

	return stem_plot


# BOO!