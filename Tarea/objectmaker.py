#Domingo Mora
#A01783317
import sys
import math

def generate_wheel_data(num_sides, radius, width):
    num_sides = max(3, min(num_sides, 360))
    vertices = []
    faces = []

    # Generate the outer vertices
    for i in range(num_sides):
        angle = 2 * math.pi * i / num_sides
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        mm = width / 2
        mm1 = -width / 2

        vertices.append((x, y, mm))
        vertices.append((x, y, mm1))
    vertices.append((0,0,mm))
    vertices.append((0,0,mm1))

    # Generate the faces
    for i in range(num_sides):
        # Generate the faces

        if i == 0:
            faces.append([i*2, i*2+1, num_sides*2+1])
            faces.append([i*2, num_sides*2+1, num_sides*2])
            faces.append([num_sides*2+1, i*2+1, num_sides*2+2])
            faces.append([i*2, num_sides*2, num_sides*2+2])
        else:
            faces.append([i*2, i*2+1, i*2-2])
            faces.append([i*2, i*2-2, i*2-4])
            faces.append([i*2-2, i*2+1, num_sides*2+2])
            faces.append([i*2, i*2-4, num_sides*2+2])
    return vertices, faces

def cross_product(v1, v2):
    cp = [v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0],]
    #magnitude to normalize cross product
    mag = math.sqrt(cp[0]**2 + cp[1]**2 + cp[2]**2)
    if mag != 0:
        cp[0] /= mag
        cp[1] /= mag
        cp[2] /= mag
        return cp
    else:
        return [0, 0, 0]
    
#calculate normals of the faces
def calculate_normals(vertices, faces):
    normals = []
    fn = []
    v1 = [0, 0, 0]
    v2 = [0, 0, 0]
    for face in faces:
        v1[0] = vertices[face[0] - 1][0] - vertices[face[1] - 1][0]
        v1[1] = vertices[face[0] - 1][1] - vertices[face[1] - 1][1]
        v1[2] = vertices[face[0] - 1][2] - vertices[face[1] - 1][2]
        v2[0] = vertices[face[0] - 1][0] - vertices[face[2] - 1][0]
        v2[1] = vertices[face[0] - 1][1] - vertices[face[2] - 1][1]
        v2[2] = vertices[face[0] - 1][2] - vertices[face[2] - 1][2]
        a = cross_product(v1, v2)
        if a not in normals:
            normals.append(a)
        fn.append(normals.index(a)+1)
    return normals, fn

def merge_nf(normals, faces):
    merged_faces = []
    for i in range(len(faces)):
        if i < len(normals):  # Check if the index is within the range of normals
            merged_faces.append(faces[i] + [normals[i]])
        else:
            print(f"Index {i} is out of range for normals.")
    return merged_faces

# Create the .obj file
def create_file(filename, vertices, faces, normals, fn):
    with open(filename, 'w') as obj_file:
        obj_file.write("# 3D Wheel in .obj format\n")
        # Calculate the normal
        normal = calculate_normals(vertices, faces)
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]:.4f} {vertex[1]:.4f} {vertex[2]:.4f}\n")
        for normal in normals:
            if isinstance(normal, list) and len(normal) >= 3:
                obj_file.write(f"vn {normal[0]:.4f} {normal[1]:.4f} {normal[2]:.4f}\n")
            else:
                print(f'Invalid normal: {normal}')
        for face in faces:
            obj_file.write("f")
            for v_idx in face:
                obj_file.write(f" {v_idx}")
            obj_file.write("\n")

if __name__ == "__main__":
    num_sides = int(input("Enter the number of sides (3-360): "))
    radius = float(input("Enter the radius of the wheel: "))
    width = float(input("Enter the width of the wheel: "))
    vertices, faces = generate_wheel_data(num_sides, radius, width)
    normals, fn = calculate_normals(vertices, faces)
    faces = merge_nf(normals, faces)
    create_file("wheelT.obj", vertices, faces, normals, fn)

