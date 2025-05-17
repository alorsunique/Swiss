import numpy as np
import matplotlib.pyplot as plt

def fractal_sierpinski(point_1, point_2):

    point_1_x = point_1[0]
    point_1_y = point_1[1]


    point_2_x = point_2[0]
    point_2_y = point_2[1]


    print(f"{point_1_x} {point_1_y}")
    print(f"{point_2_x} {point_2_y}")

    difference_vector = (point_2_x-point_1_x,point_2_y-point_1_y)

    mag_difference_vector = np.sqrt((difference_vector[0])**2 + (difference_vector[1])**2)

    print(difference_vector)
    print(mag_difference_vector)

    angle_from_x = np.arctan2(difference_vector[1],difference_vector[0])

    print(angle_from_x)





    fractal_point_1 = (0,0)
    fractal_point_2 = (1/3,0)
    fractal_point_3 = (0.5,np.sqrt(3)/2)
    fractal_point_4 = (2/3,0)
    fractal_point_5 = (1,0)

    point_list = [fractal_point_1,fractal_point_2,fractal_point_3,fractal_point_4,fractal_point_5]

    print(fractal_point_1)
    print(fractal_point_2)
    print(fractal_point_3)
    print(fractal_point_4)
    print(fractal_point_5)

    # Rotate point first

    rotation_matrix = np.matrix([[np.cos(angle_from_x), -np.sin(angle_from_x)],[np.sin(angle_from_x), np.cos(angle_from_x)]])
    print(rotation_matrix)

    rotated_point_list = []

    print("HEY")

    for point in point_list:

        rotated_point_matrix_object = np.dot(rotation_matrix,[point[0],point[1]])
        rotated_list_matrix_list = rotated_point_matrix_object.tolist()

        rotated_point = (rotated_list_matrix_list[0][0], rotated_list_matrix_list[0][1])
        print(rotated_point)
        rotated_point_list.append(rotated_point)

    # Scale

    scaled_point_list = []

    for point in rotated_point_list:
        print(point)

        scaled_point = (mag_difference_vector*point[0],mag_difference_vector*point[1])
        print(scaled_point)

        scaled_point_list.append(scaled_point)

    # Translate

    translate_point_list = []

    for point in scaled_point_list:
        print(point)

        translate_point = (point_1_x+point[0],point_1_y+point[1])
        print(translate_point)
        translate_point_list.append(translate_point)

    return translate_point_list




first_point = (0,0)
second_point = (1,0)


point_list = fractal_sierpinski(first_point,second_point)

x_list = []
y_list = []

for point in point_list:
    x_list.append(point[0])
    y_list.append(point[1])


print(point_list)

plt.plot(x_list,y_list)
plt.show()
