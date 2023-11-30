import math
def fill_wheel_vertices(
    sides,
    radius,
    width,
):
    # Declare the wheel sides variable
    wheel_vertices = []

    # Add the wheel sides
    for i in range(sides):
        # Calculate the angle of the side
        angle = 2 * math.pi * i / sides
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # Add the side vertices
        wheel_vertices.append([width / 2, x, y])
        wheel_vertices.append([-width / 2, x, y])

    # Add closing sides
    wheel_vertices.append([width / 2, 0, 0])
    wheel_vertices.append([-width / 2, 0, 0])

    # Return the wheel sides
    return wheel_vertices


# Add the wheel faces
def fill_wheel_faces_and_vectors(sides):
    # Declare the wheel faces variable
    faces = []
    # Add the wheel faces
    for i in range(1, sides + 1):
        # Add the first side exception
        if i == 1:
            faces.append([i * 2, i * 2 - 1, sides * 2 - 1])
            faces.append([i * 2, sides * 2 - 1, sides * 2])
            faces.append([sides * 2 - 1, i * 2 - 1, sides * 2 + 1])
            faces.append([i * 2, sides * 2, sides * 2 + 2])
        # Add the last side exception
        else:
            faces.append([i * 2, i * 2 - 1, i * 2 - 3])
            faces.append([i * 2, i * 2 - 3, i * 2 - 2])
            faces.append([i * 2 - 3, i * 2 - 1, sides * 2 + 1])
            faces.append([i * 2, i * 2 - 2, sides * 2 + 2])
    # Return the wheel faces
    return faces


# Calculate the cross product of two vectors and normalize the result
def calculate_cross_product_and_normalize(v1, v2):
    # Calculate the cross product of two vectors
    cross_product = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]
    # Calculate the length of the cross product vector
    length = sum([i*2 for i in cross_product]) * 0.5
    # Normalize the cross product vector
    normalized_vector = [i / length for i in cross_product]
    return normalized_vector


# Calculate the normals of the faces
def calculate_faces_normals(faces, vertices):
    normals = []
    face_normal = []
    v1 = [0, 0, 0]
    v2 = [0, 0, 0]
    # Calculate the normals of the faces
    for face in faces:
        v1[0] = vertices[face[0] - 1][0] - vertices[face[1] - 1][0]
        v1[1] = vertices[face[0] - 1][1] - vertices[face[1] - 1][1]
        v1[2] = vertices[face[0] - 1][2] - vertices[face[1] - 1][2]
        v2[0] = vertices[face[0] - 1][0] - vertices[face[2] - 1][0]
        v2[1] = vertices[face[0] - 1][1] - vertices[face[2] - 1][1]
        v2[2] = vertices[face[0] - 1][2] - vertices[face[2] - 1][2]

        normal = calculate_cross_product_and_normalize(v1, v2)
        # Add the list of normals if it is not already in the list
        if normal not in normals:
            normals.append(normal)
        # Add the index of the normal to the face to be able to reference it later
        face_normal.append(normals.index(normal) + 1)
    return normals, face_normal


# Merge the normals and the faces
def merge_normals_and_faces(normals, faces):
    # Add the normals to the faces
    for i in range(len(faces)):
        faces[i].append(normals[i])
    return faces