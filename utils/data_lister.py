import os
 
# prints parent directory
project_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

ignore = ["static"]

data = []
for f in os.listdir(str(project_dir) + "/assets/"):
    if f not in ignore :
        for file in os.listdir(str(project_dir) + "/assets/" + f + "/"):
            if '.png' in file :
                data.append(f + "/" + file)
print(data)