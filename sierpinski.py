import numpy as np
import matplotlib.pyplot as plt

def fractal_sierpinski(point_1, point_2):

    point_1_x = point_1[0]
    point_1_y = point_1[1]


    point_2_x = point_2[0]
    point_2_y = point_2[1]


    print(f"Point 1 | x: {point_1_x} | y: {point_1_y}")
    print(f"Point 2 | x: {point_2_x} | y: {point_2_y}")

    difference_vector = (point_2_x-point_1_x,point_2_y-point_1_y)
    mag_difference_vector = np.sqrt((difference_vector[0])**2 + (difference_vector[1])**2)

    angle_from_x = np.arctan2(difference_vector[1],difference_vector[0])

    print(f"Difference Vector: {difference_vector} | Magnitude: {mag_difference_vector} | Angle: {angle_from_x}")


    fractal_point_1 = (0,0)
    fractal_point_2 = (1/3,0)
    fractal_point_3 = (0.5,(np.sqrt(3)/2)/3)
    fractal_point_4 = (2/3,0)
    fractal_point_5 = (1,0)

    point_list = [fractal_point_1,fractal_point_2,fractal_point_3,fractal_point_4,fractal_point_5]

    # Rotate point first

    rotation_matrix = np.matrix([[np.cos(angle_from_x), -np.sin(angle_from_x)],[np.sin(angle_from_x), np.cos(angle_from_x)]])
    rotated_point_list = []

    for point in point_list:

        rotated_point_matrix_object = np.dot(rotation_matrix,[point[0],point[1]])
        rotated_list_matrix_list = rotated_point_matrix_object.tolist()

        rotated_point = (rotated_list_matrix_list[0][0], rotated_list_matrix_list[0][1])
        rotated_point_list.append(rotated_point)

    # Scale

    scaled_point_list = []

    for point in rotated_point_list:
        scaled_point = (mag_difference_vector*point[0],mag_difference_vector*point[1])
        scaled_point_list.append(scaled_point)

    # Translate

    translate_point_list = []

    for point in scaled_point_list:

        translate_point = (point_1_x+point[0],point_1_y+point[1])
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




plt.plot(x_list,y_list)
plt.show()



iteration = 1

third_point = (2,0)

working_points = [first_point, second_point,third_point]

count = 0

pair_working_points = []

while count < len(working_points)-1:
    pair = [working_points[count], working_points[count+1]]
    pair_working_points.append(pair)
    count += 1

print(pair_working_points)

iteration_max = 4

iteration_count = 0



working_points = [first_point, second_point]

first_point = (-0.5,0)
half_first = (0,0)
second_point = (0.5,0)
half_second = ((0.5+0)/2, (np.sqrt(3)/2)/2)
third_point = (0,np.sqrt(3)/2)
half_third = ((-0.5+0)/2, (np.sqrt(3)/2)/2)


working_points = [first_point, half_first,second_point, half_second,third_point, half_third, first_point]

while iteration_count < iteration_max:
    iteration_count += 1

    count = 0

    pair_working_points = []

    while count < len(working_points) - 1:



        pair = [working_points[count], working_points[count + 1]]

        print(f"Iteration: {iteration_count} | Pair: {pair}")

        pair_working_points.append(pair)
        count += 1

    working_points = []

    for pair in pair_working_points:

        translated_work_point = fractal_sierpinski(pair[0],pair[1])

        print(f"Generated Point: {translated_work_point}")

        for entry in translated_work_point:
            working_points.append(entry)


    trimmed_working_point = []

    count = 0

    while count < len(working_points)-1:
        if working_points[count] != working_points[count+1]:
            trimmed_working_point.append(working_points[count])
        count += 1

    trimmed_working_point.append(working_points[-1])

    print(f"Iteration Output List: {trimmed_working_point}")

    working_points = trimmed_working_point


x_list = []
y_list = []

for point in working_points:
    x_list.append(point[0])
    y_list.append(point[1])

plt.xlim(-2, 2)
plt.ylim(-2, 2)

plt.gca().set_aspect('equal', adjustable='box')

plt.plot(x_list,y_list)
plt.show()
