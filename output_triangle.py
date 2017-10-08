import cv2
import numpy

tri_curry = open("tri_curry.txt") # triangle point
curry_point = open("Curry.txt")   # curry correspond point
output = open("tri_ans.txt","w")
data1 = []
points_curry = []

# store correspond point in curry_point
for line in curry_point:
    x, y = line.split()
    points_curry.append((int(x), int(y)))

# store triangle points in tri_curry
for line in tri_curry:
    a,b,c = line.split(";")

    x1,y1 = a.split(" ")
    data1.append((int(x1),int(y1)))



    x2, y2 = b.split(" ")

    x3, y3 = c.split(" ")

    i = 0
    j = 0
    k = 0
    # loop and get the series number of each points of triangles, then saved series number into tri_ans.txt
    temp = []
    while i < 46:

        if int(x1) == points_curry[i][0] and int(y1) == points_curry[i][1]:
            print(i)
            temp.append(i)
            print(points_curry[i])
        i += 1
    while j < 46:

        if int(x2) == points_curry[j][0] and int(y2) == points_curry[j][1]:
            print(j)
            temp.append(j)
            print("!!!!!!")
            print(points_curry[j])
        j += 1
    while k < 46:

        if int(x3) == points_curry[k][0] and int(y3) == points_curry[k][1]:
            print(k)
            temp.append(k)
            print("!!!!!!")
            print(points_curry[k])
        k += 1
    output.write(str(temp[0])+" "+str(temp[1])+" "+str(temp[2])+"\n")

output.close()


