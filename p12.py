import numpy as np
from skimage.measure import label
from scipy.ndimage import convolve


PLUS = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
CORNERS = [
    np.array([[0, 1, 1], [0, -3, 1], [0, 0, 0]]),
    np.array([[0, 0, 0], [0, -3, 1], [0, 1, 1]]),
    np.array([[0, 0, 0], [1, -3, 0], [1, 1, 0]]),
    np.array([[1, 1, 0], [1, -3, 0], [0, 0, 0]]),
    np.array([[0, -1, 3], [0, 0, -1], [0, 0, 0]]),
    np.array([[0, 0, 0], [0, 0, -1], [0, -1, 3]]),
    np.array([[0, 0, 0], [-1, 0, 0], [3, -1, 0]]),
    np.array([[3, -1, 0], [-1, 0, 0], [0, 0, 0]]),
]

def ingest_p12(fname):
    with open(fname, "r") as f:
        lines = f.readlines()

    data = np.array([[ord(c) for c in line.strip()] for line in lines])

    return data


def p12a(data):
    # Label the regions
    # Add padding to make our perimeter calculation work for regions on the border
    labels, nlabels = label(np.pad(data, 1), return_num=True, connectivity=1)

    # Calculate areas by summing binary arrays, and perimeters by
    # convolving with a plus-shaped kernel
    totalprice = 0
    for labelval in range(1, nlabels + 1):
        binarr = (labels == labelval)
        area = binarr.sum()
        edgearr = convolve(binarr.astype(int), PLUS)
        edgearr[binarr] = 0
        perimeter = edgearr.sum()
        totalprice += area * perimeter

    return totalprice


def p12b(data):
    """Count corners, since the number of corners equals the number of
    edges. Find corners by convolving the binary array
    with the CORNERS kernels.
    """
    labels, nlabels = label(np.pad(data, 1), return_num=True, connectivity=1)

    totalprice = 0
    for labelval in range(1, nlabels + 1):
        binarr = (labels == labelval)
        area = binarr.sum()
        edgearr = np.sum([convolve(binarr.astype(int), c) == 3 for c in CORNERS], axis=0)
        ncorners = edgearr.sum()
        totalprice += area * ncorners

    return totalprice


if __name__ == "__main__":
    data = ingest_p12("data/input_p12.txt")

    print("Part 1: {}".format(p12a(data)))
    print("Part 2: {}".format(p12b(data)))
