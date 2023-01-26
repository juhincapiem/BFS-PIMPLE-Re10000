vel = open("postProcessing/probes/0/U")
lines = vel.readlines()

print(lines[11])
print(lines[24].split('('))

for i in lines[24:]:
    
