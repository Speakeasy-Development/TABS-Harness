
# Simply create a copy-paste able html input group
pattern = "<input type=\"text\" name=\"{} {}\"  maxlength=\"3\" size=\"3\">"

SizeX = 10
SizeY = 10

for x in range(0, SizeX):

    for y in range(0, SizeY):

        print(pattern.format(x, y))

    print('<br>')
