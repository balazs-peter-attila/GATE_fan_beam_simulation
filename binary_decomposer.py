import cv2
import numpy as np
from mosaic import rectangular_decomposition
from mosaic.utilities import plot_image_decomposition

#UNIT = 0.064  # in mm
UNIT = 0.2  # in mm

HEADER = """/gate/world/daughters/name encapsulatingBox
/gate/world/daughters/insert box
/gate/encapsulatingBox/geometry/setXLength 100 mm
/gate/encapsulatingBox/geometry/setYLength 100 mm
/gate/encapsulatingBox/geometry/setZLength 100 mm
/gate/encapsulatingBox/placement/setTranslation  0 0 100 mm
/gate/encapsulatingBox/setMaterial Air
/gate/encapsulatingBox/vis/forceWireframe
/gate/encapsulatingBox/vis/setColor white
/gate/encapsulatingBox/moves/insert rotation
/gate/encapsulatingBox/rotation/setSpeed 1 deg/s
/gate/encapsulatingBox/rotation/setAxis 0 1 0"""

#Write to file
f = open("d:\\phantoms\\decomposed-phantom_3-h.mac", "a")
f.write(HEADER + "\n\n")

# Materials
ALPHA = 0.9
AIR = [1, 1, 1, ALPHA]          # grey
PLASTIC = [1, 1, 0, ALPHA]      # yellow
ALUMINIUM = [0, 0, 1, ALPHA]    # blue

if __name__ == "__main__":
    image_path = "d:\\data\\phantom_3.png"

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    #object is assumed to be black
#    binary_image = np.logical_not(image.astype(bool)).astype(int)
    binary_image = image.astype(bool).astype(int)
#    comment out below line for vertical decomposition
    binary_image = np.rot90(binary_image)
    imagesize_y, imagesize_x = binary_image.shape
    y_offset = round(imagesize_y / 2, 3)
    x_offset = round(imagesize_x / 2, 3)
    print(f"offset_y:{y_offset}, offset_x: {x_offset}")
    num_zeros = np.count_nonzero(binary_image == 0)
    rectangles = rectangular_decomposition(binary_image)
    #print("Identified rectangles:", rectangles)
    for index, rect in enumerate(rectangles):
        y_size = round(UNIT * round(rect.y_end - rect.y_start + 1, 2), 3)
        x_size = round(UNIT * round(rect.x_end - rect.x_start + 1, 2), 3)
        y_corner = round(UNIT * round(rect.y_start - y_offset, 2), 3)
        x_corner = round(UNIT * round(rect.x_start - x_offset, 2), 3)
        y_center = round(y_corner + y_size/2, 3)
        x_center = round(x_corner + x_size/2, 3)
        print(f"{y_corner}, {x_corner}, {y_center}, {x_center}, {y_size}, {x_size}")
        voxelname = "voxel_" + str(index + 1).zfill(4)
        materialname = "Plastic"
        materialcolor = "yellow"
        f.write("/gate/encapsulatingBox/daughters/name " + voxelname + "\n")
        f.write("/gate/encapsulatingBox/daughters/insert box\n")
        f.write("/gate/" + voxelname + "/geometry/setXLength " + str(y_size) + " mm\n")
        f.write("/gate/" + voxelname + "/geometry/setYLength 1 mm\n")
        f.write("/gate/" + voxelname + "/geometry/setZLength " + str(x_size) + " mm\n")
        f.write("/gate/" + voxelname + "/setMaterial " + materialname + "\n")
        f.write("/gate/" + voxelname + "/vis/forceSolid\n")
        f.write("/gate/" + voxelname + "/vis/setColor " + materialcolor + "\n")
        f.write("/gate/" + voxelname + "/placement/setTranslation " + str(y_center) + ' 0 ' + str(x_center) + " mm\n\n")

    print("Number of object pixels:", num_zeros)
    print("Number of rectangles:", len(rectangles))

    plot_image_decomposition(binary_image, rectangles=rectangles)


# unique_elements, counts = np.unique(array_2d, return_counts=True)