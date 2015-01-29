f = open("domusdomezones.svg", "r")
svg = []
for line in f:
    line = line.strip()
    svg.append(line)
f.close()

vector_paths = []
for i in range(0, len(svg)):
    if svg[i] == "<path":# spot the paths location 
        i = i+1 
        svg[i] = svg[i].replace(',', ' ')# remove the first 5 items in each path, replace  spaces with commas
        svg[i] = svg[i][5:-1].split(' ')# remove the first 5 and the last item of the line of each path, split each vector into a iterable list
        vector_paths.append(svg[i])

paths = []
for n in range(0, len(vector_paths)):
    paths.append(vector_paths[n])
    for m in range(0, len(vector_paths[n])):
        vector_paths[n][m] = float(vector_paths[n][m]) # float all strings of the vector_paths list 
for p in range(0, len(paths)):
    for o in range(2, len(paths[p])-1):# loop to sum vectors
        paths[p][o] = paths[p][o-2] + paths[p][o]# sum the vectors of each cordinate
    for o in range(0, len(paths[p])):#loop to round each cordinate
        paths[p][o] = round(paths[p][o],2) #round the floating points to a two decimal float  
print paths 
