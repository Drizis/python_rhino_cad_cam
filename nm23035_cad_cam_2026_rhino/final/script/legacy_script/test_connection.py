import rhinoscriptsyntax as rs

# 1. Create two points
pt1 = [0, 0, 0]
pt2 = [10, 10, 10]

# 2. Draw a line between them
line_id = rs.AddLine(pt1, pt2)

# 3. Print a message to the console
print("Success! The line was created in Rhino.")