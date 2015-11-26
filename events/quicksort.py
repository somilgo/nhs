def quicksort(toSort, start=0, end=-1):
	arr = toSort
	if end == -1:
		end = len(arr) - 1
	if (end-start) <= 0:
		return arr
	pivot = arr[end]
	wall = start
	for i in range(start, end):
		if get_time(pivot) <= get_time(arr[i]):
			pass
		else:
			temp = arr[i]
			arr[i] = arr[wall]
			arr[wall] = temp
			wall+=1
	temp = arr[wall]
	arr[wall] = pivot
	arr[end] = temp
	return quicksort(quicksort(arr, start, wall-1), wall+1, end)

def get_time(i):
	return int(i.start_time.hour) + int(i.start_time.minute)/100.0