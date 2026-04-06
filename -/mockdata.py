import re


with open("mockdata.txt", "r", encoding="utf-8") as f, \
     open("name.txt", "w", encoding="utf-8") as name_file, \
     open("surname.txt", "w", encoding="utf-8") as surname_file, \
     open("typeFile.txt", "w", encoding="utf-8") as type_file:

    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")

        name_file.write(parts[0] + "\n")
        surname_file.write(parts[1] + "\n")

        
        type_match = re.search(r'\.(\w+)$', parts[3])
        if type_match:
            type_file.write(type_match.group(1) + "\n")
