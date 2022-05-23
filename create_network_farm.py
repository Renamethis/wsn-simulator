from json import dump
map_size = (300, 300)
clusters = 3
data = {}
data['clusters'] = []
data['map_size'] = map_size
y = 50
for i in range(clusters):
    y+=70
    x=10
    data['clusters'].append({})
    data['clusters'][i]['centroid'] = (150, y)
    data['clusters'][i]['devices'] = []
    headpos = None
    for j in range(9):
        x+=28
        data['clusters'][i]['devices'].append({
            'pos': (x, y),
            'initial_energy': 1,
            'coverage': 15
        })
        if(j == 5):
            headpos = (x, y)
    data['clusters'][i]['head'] = {
        'pos':headpos,
        'initial_energy': 1,
        'coverage': 15
    }
data['station'] = {
    'pos': (150, 150)
}
with open('networks/farm1.json', 'w') as f:
    dump(data, f)