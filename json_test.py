import json
# create json
data = {
    "president": {
        "name":"mr prezident",
        "city":"moscow"
    }
}
# # write json
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4) # indent - otstup
count =0
# Read Json
with open('sample2.json', 'r', encoding = 'utf-8') as f:
    data = json.load(f)
    # Take info from Json by Key name
    for name in data:
        name['age']

        count +=1
        one_digit = (int(count))
        print(one_digit)


