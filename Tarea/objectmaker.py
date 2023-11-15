#Domingo Mora
#A01783317
import sys
import math

def generate_wheel_data(num_sides, radius, width):
    num_sides = max(3, min(num_sides, 360))

    vertices = []
    normals = []
    faces = []

    # Generate the center vertices
    center_vertices = [(0, 0, width / 2), (0, 0, -width / 2)]
    vertices.extend(center_vertices)
    normals.extend([(1, 0, 0), (1, 0, 0)])

    # Generate the outer vertices
    for i in range(num_sides):
        angle = 2 * math.pi * i / num_sides
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        mm = -width / 2
        mm1 = width / 2

        vertices.append((x, y, mm))
        vertices.append((x, y, mm1))
    vertices.append((0,0,mm))
    vertices.append((0,0,mm1))
    

    for i in range(num_sides):
        v1 = i * 2
        v2 = i * 2 + 1
        v3 = (i * 2 + 2) % (num_sides * 2)
        v4 = (i * 2 + 3) % (num_sides * 2)
        v5 = num_sides * 2 + 1
        v6 = num_sides * 2

        faces.append([v4, v2, v1])
        faces.append([v1, v3, v4])
        faces.append([v3, v1, v5])
        faces.append([v4, v6, v2])

    # Generate two additional faces for the center vertices
    center_start = len(vertices) - 2
    faces.extend([  
    center_start, center_start + 1, len(vertices), center_start + 3, center_start + 2, len(vertices) + 1,
    len(vertices), len(vertices) + 1, 1, 3, 2, 0
])
    return vertices, normals, faces

def create_obj_file(vertices, normals, faces, output_file="wheelTRI.obj"):
    with open(output_file, 'w') as obj_file:
        obj_file.write("# 3D Wheel in .obj format\n")

        for vertex in vertices:
            obj_file.write(f"v {vertex[0]:.4f} {vertex[1]:.4f} {vertex[2]:.4f}\n")
        for normal in normals:
            obj_file.write(f"vn {normal[0]:.4f} {normal[1]:.4f} {normal[2]:.4f}\n")
        for face in faces:
            obj_file.write(f"f {face[0]+1}//{face[0]+1} {face[1]+1}//{face[1]+1} {face[2]+1}//{face[2]+1}\n")


if __name__ == "__main__":
    num_sides = int(input("Enter the number of sides (3-360): "))
    radius = float(input("Enter the radius of the wheel: "))
    width = float(input("Enter the width of the wheel: "))

    vertices, normals, faces = generate_wheel_data(num_sides, radius, width)
    create_obj_file(vertices, normals, faces)
