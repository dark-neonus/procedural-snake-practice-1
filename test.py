import triangulator
import triangulator.ear_clipping_method

pre_list = ((1, 1), (4, 2), (3, 2), (2, 7), (3, 4), (7, 3), (8, 3), (9, 0))
pre_list = ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0))
print("pre_list:", pre_list)

triangles = triangulator.ear_clipping_method.triangulate(pre_list)

print("triangles:", triangles)