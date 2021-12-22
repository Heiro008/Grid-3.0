import pandas

def path(x,data):
	if data['Destination'][x][0] == 'M':
		return 0
	elif data['Destination'][x][0] == 'D':
		return 1
	elif data['Destination'][x][0] == 'K':
		return 2
	elif data['Destination'][x][0] == 'C':
		return 3
	elif data['Destination'][x][0] == 'B':
		return 4
	elif data['Destination'][x][0] == 'H':
		return 5
	elif data['Destination'][x][0] == 'P':
		return 6
	elif data['Destination'][x][0] == 'A':
		return 7
	elif data['Destination'][x][0] == 'J':
		return 8
def parse_excel_data():
	data = pandas.read_excel('package_list.xls')
	data['path_no'] = [path(i,data) for i in range(data.shape[0])]

	zone1 = data.query('InductStation==1')
	zone2 = data.query('InductStation==2')
	path_nos = list()
	path_nos.append(list(zone1['path_no']))
	path_nos.append(list(zone2['path_no']))
	del data,zone1,zone2
	print('zone 1:')
	print(path_nos[0])
	print('zone 2:')
	print(path_nos[1])
	return path_nos