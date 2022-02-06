import json

with open('results.txt', 'r', encoding='utf8') as txt:
	lines = txt.readlines()
	lines.append('')
	temp = ''

	sauce, data, uid = {}, {}, []
	final = {}

	count = 0

	for n in range(len(lines)):
		temp = lines[n].strip()

		if n % 8 == 0:
			sauce, data = {}, {}
			data['name'] = temp
		else:
			if n % 8 == 7: # newline
				count += 1
				data["_id"] = count
				data["sauce"] = sauce
				uid.append(data)
			else:
				temp = temp.strip('][').split(', ')
				sauce[n % 8] = temp

	final["sauces"] = uid


	with open('results.json', 'w', encoding='utf8') as out:
		json.dump(final, out, indent=4, sort_keys=True)
