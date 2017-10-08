import cv2
import numpy as np




# Check if a point is inside a rectangle
def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


# Draw a point
def draw_point(img, p, color):
    # cv2.circle( img, p, 2, color, cv2.cv.CV_FILLED, cv2.LINE_AA, 0 )
    cv2.circle(img, p, 2, color, 1, cv2.LINE_AA, 0)


# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color, points):
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])
    temp = 1

    # output_file = open("tri.txt", 'w')
    output_file = open("tri_curry.txt", 'w')
    for t in triangleList:

        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)

            output_string = str(pt1[0])+" "+str(pt1[1])+";"+str(pt2[0])+" "+str(pt2[1])+";"+str(pt3[0])+" "+str(pt3[1]) + "\n"
            output_file.write(output_string)

            print(temp)
            temp+=1







            print("-----")
    output_file.close()




if __name__ == '__main__':

    # Define window names
    win_delaunay = "Delaunay Triangulation"

    # Turn on animation while drawing triangles
    animate = True

    # Define colors for drawing.
    delaunay_color = (255, 255, 255)
    points_color = (0, 0, 255)

    # Read in the image.
    img = cv2.imread("Curry.png")

    # Keep a copy around
    img_orig = img.copy();

    # Rectangle to be used with Subdiv2D
    size = img.shape
    print(size)

    rect = (0, 0, size[1], size[0])

    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect);

    # Create an array of points.
    points = [];
    with open("Curry.txt") as file:
        for line in file:
            x, y = line.split()
            points.append((int(x), int(y)))
    print(points[1])
    print(points[1][1])

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

        # Show animation
        if animate:
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay(img_copy, subdiv, (255, 255, 255),points);
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

    # Draw delaunay triangles
    draw_delaunay(img, subdiv, (255, 255, 255),points);

    # Draw points
    for p in points:
        draw_point(img, p, (0, 0, 255))


    # Show results
    cv2.imshow(win_delaunay, img)
    cv2.waitKey(0)


