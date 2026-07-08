#筛选高度大于10，放进list1
list = [12.5,8.0,25.3,6.2,15.0,9.8]
list1 = []

for i in list:
    if i > 10:
        list1.append(i)

print(f'buiding height > 10m is:',(list1))
#厘米转化为米
list2 = []
for i in list:
    m = i*100
    n = int(m)
    list2.append(n)

print(f'convert buiding height to centimeter is:',(list2))
#给list加0，1，2，3...（(i,h) for i, h in enumerate()
pairs = [(i, h) for i, h in enumerate(list)]
print(pairs)

buildings = [
    {"id": "B1", "type": "residential", "height": 12.5},
    {"id": "B2", "type": "office", "height": 25.3},
    {"id": "B3", "type": "residential", "height": 8.0}
]

#分组grouped
grouped = {}
for b in buildings:
    key = b["type"]
    if key not in grouped:
        grouped[key] = []
    grouped[key].append(b)

print(grouped)

#统计平均高度，heights = [b[height] for b in group]
stats = {}
for type_name,group in grouped.items():
    heights = [b["height"]for b in group]
    stats[type_name] = {
        "count": len(group),
        "avg_height": sum(heights)/len(heights)
    }