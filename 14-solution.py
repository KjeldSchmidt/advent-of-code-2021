from collections import Counter, defaultdict

template = "HBHVVNPCNFPSVKBPPCBH"

transformations = {}
with open("14-input.txt") as f:
    for line in f.readlines():
        line = line.strip().split(" -> ")
        transformations[line[0]] = line[1]

for _ in range(10):
    new_template = []
    for i in range(len(template)-1):
        letters = template[i:i+2]
        new_template.append(letters[0])
        new_template.append(transformations.get(letters, ""))
    new_template.append(template[-1])
    template = "".join(new_template)

freq = dict(Counter(template))
freq = {v: k for k, v in freq.items()}

print("Solution part 1:")
print(max(freq) - min(freq))


template = "HBHVVNPCNFPSVKBPPCBH"
material_counts = defaultdict(lambda: 0)
for i in range(len(template) - 1):
    letters = template[i:i+2]
    material_counts[letters] += 1

for _ in range(40):
    new_counts = defaultdict(lambda: 0)
    for k, v in material_counts.items():
        if k in transformations:
            new_material = transformations[k]
            left = k[0] + new_material
            right = new_material + k[1]
            new_counts[left] += v
            new_counts[right] += v
        else:
            new_counts[k] = v

    material_counts = new_counts


freq = defaultdict(lambda: 0)
for material, count in material_counts.items():
    freq[material[0]] += count
    freq[material[1]] += count
freq = {v: k for k, v in freq.items()}

offset = 0
if freq[min(freq)] == template[0]:
    offset = -1
elif freq[max(freq)] == template[0]:
    offset = 1

print("Solution part 2:")
print((max(freq) - min(freq))//2 + offset)
