import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

# get area of triangle ABC
def AreaOfTriangle(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

# return true if point P is in triangle ABC
def InTriangle(x1, y1, x2, y2, x3, y3, x, y):
    # square of triangle ABC
    ABC = AreaOfTriangle(x1, y1, x2, y2, x3, y3)

    # square of triangle PBC
    PBC = AreaOfTriangle(x, y, x2, y2, x3, y3)

    # square of triangle PAC
    PAC = AreaOfTriangle(x1, y1, x, y, x3, y3)

    # square of triangle PAB
    PAB = AreaOfTriangle(x1, y1, x2, y2, x, y)
    return (ABC == PBC + PAC + PAB)


# morph processing 1. get correspond point in file 2. curry -> morph 3. durant -> morph 4. merge
def Morph(image1_path, image2_path, image1_point_path, image2_point_path,dir,alpha):

    img_curry = cv2.imread(image1_path)
    img_durant = cv2.imread(image2_path)

    img_curry = np.float32(img_curry)
    img_durant = np.float32(img_durant)


    # save correspond point
    curry_point = []
    with open(image1_point_path) as curry_file:
        for line in curry_file:
            x, y = line.split()
            curry_point.append((int(x), int(y)))

    durant_point = []
    with open(image2_point_path) as durant_file:
        for line in durant_file:
            x, y = line.split()
            durant_point.append((int(x), int(y)))

    morph_point = []
    for i in range(0, 46):
        x = (1 - alpha) * durant_point[i][0] + alpha * curry_point[i][0]
        y = (1 - alpha) * durant_point[i][1] + alpha * curry_point[i][1]
        morph_point.append((x, y))

    img_morph1 = np.zeros(img_curry.shape, dtype=img_curry.dtype)
    img_morph2 = np.zeros(img_durant.shape, dtype=img_durant.dtype)

    # get curry and durant file's image from each triangle
    with open("tri_ans.txt") as file:
        for line in file:
            a, b, c = line.split()
            p_curry = [curry_point[int(a)], curry_point[int(b)], curry_point[int(c)]]
            p_durant = [durant_point[int(a)], durant_point[int(b)], durant_point[int(c)]]
            p_morph = [morph_point[int(a)], morph_point[int(b)], morph_point[int(c)]]



            # x1,x2,x3,y1,y2,y3 curry
            x1 = p_curry[0][0]
            y1 = p_curry[0][1]
            x2 = p_curry[1][0]
            y2 = p_curry[1][1]
            x3 = p_curry[2][0]
            y3 = p_curry[2][1]

            # m1,m2,m3,k1,k2,k3 durant
            m1 = p_durant[0][0]
            k1 = p_durant[0][1]
            m2 = p_durant[1][0]
            k2 = p_durant[1][1]
            m3 = p_durant[2][0]
            k3 = p_durant[2][1]

            # X1,X2,X3,Y1,Y2,Y3
            X1 = p_morph[0][0]
            Y1 = p_morph[0][1]
            X2 = p_morph[1][0]
            Y2 = p_morph[1][1]
            X3 = p_morph[2][0]
            Y3 = p_morph[2][1]

            # calculate affine matrix

            matrix_curry = np.matrix([[x1, x2, x3], [y1, y2, y3], [1, 1, 1]])
            matrix_durant = np.matrix([[m1,m2,m3], [k1,k2,k3], [1,1,1]])
            matrix_morph = np.matrix([[int(X1), int(X2), int(X3)], [int(Y1), int(Y2), int(Y3)], [1, 1, 1]])

            # affine matrix
            ans1 = matrix_morph * (matrix_curry.T) * ((matrix_curry * (matrix_curry.T)) ** -1)
            ans2 = matrix_morph * (matrix_durant.T) * ((matrix_durant * (matrix_durant.T)) ** -1)


            tempX = 0
            while tempX < 260:
                tempY = 0
                while tempY < 190:
                    # find all points in triangle
                    if InTriangle(x1, y1, x2, y2, x3, y3, tempX, tempY):

                        ans_point = np.matrix([[tempX], [tempY], [1]])
                        ans_point_matrix = ans1 * ans_point

                        if int(ans_point_matrix[1, 0]) < 190 and int(ans_point_matrix[0, 0]) < 260:
                            img_morph1[int(ans_point_matrix[1, 0])][int(ans_point_matrix[0, 0])] = img_curry[tempY][
                                tempX]
                    if InTriangle(m1,k1,m2,k2,m3,k3,tempX,tempY):

                        ans_point = np.matrix([[tempX], [tempY], [1]])
                        ans_point_matrix = ans2 * ans_point

                        if int(ans_point_matrix[1, 0]) < 190 and int(ans_point_matrix[0, 0]) < 260:
                            img_morph2[int(ans_point_matrix[1, 0])][int(ans_point_matrix[0, 0])] = img_durant[tempY][
                                tempX]

                    tempY += 1
                tempX += 1
    text1 = 0

    while text1 < 190:
        text2 = 0
        while text2 < 260:

            img_morph1[text1][text2][0] = int((1-alpha)*(img_morph1[text1][text2][0]) + alpha*(img_morph2[text1][text2][0]))
            img_morph1[text1][text2][1] = int((1-alpha)*(img_morph1[text1][text2][1]) + alpha*(img_morph2[text1][text2][1]))
            img_morph1[text1][text2][2] = int((1-alpha)*(img_morph1[text1][text2][2]) + alpha*(img_morph2[text1][text2][2]))

            # alpha blending
            img_morph1[text1][text2][0] = 255 - img_morph1[text1][text2][0]
            img_morph1[text1][text2][1] = 255 - img_morph1[text1][text2][1]
            img_morph1[text1][text2][2] = 255 - img_morph1[text1][text2][2]




            

            text2 += 1
        text1 += 1
    # image save
    new_im = plt.imshow(img_morph1)
    plt.savefig(str(dir)+"/"+str(alpha)+".png")
    # plt.show(new_im)

    
    


if __name__ == '__main__':

    i = 0.1
    while i <= 1:
        Morph("Curry.png","Durant.png","Curry.txt","Durant.txt","curry_durant",i)
        Morph("Durant.png", "Green.png", "Durant.txt", "Green.txt","durant_green", i)

        i+=0.1



    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo",0.1)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.2)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.3)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.5)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.6)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.7)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.8)
    Morph("Green.png", "Igo.png", "Green.txt", "Igo.txt", "green_igo", 0.9)



    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson", 0.1)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson", 0.2)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson", 0.3)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt", "igo_thompson",0.4)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson" ,0.6)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson" ,0.7)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson" ,0.8)
    Morph("Igo.png", "Thompson.png", "Igo.txt", "Thompson.txt","igo_thompson",0.9)





