# import module, mpimg is for testing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# takes an image im as input, and outputs a heart-shaped cut-out of the image on a pink background
# Note: here we use the RGB value [255, 192, 203] for the pink color
# Note: the heart-shape depends on the dimensions of the input image
# remark: this function works 100% perfectly with the image provided in class
# image: kitty-cat.jpg 1920 * 1439
def heart(im):
    imgc = im.copy()
    width = imgc.shape[0]
    height = imgc.shape[1]
    x, y = np.ogrid[0:width, 0:height]

    # create four masks for the shape cutting
    mask = (x - height / 4.0 > y)
    imgc[mask] = [255, 192, 203]

    mask = (-x + height / 4.0 + height < y)
    imgc[mask] = [255, 192, 203]

    mask = (x < -(height / 4.0) * np.sin(y * np.pi / (height/2.0)) + height / 4.0) & (y < height / 2.0)
    imgc[mask] = [255, 192, 203]

    mask = (x < -(height / 4.0) * np.sin(y * np.pi / (height/2.0) - np.pi) + height / 4.0) & (y > height / 2.0)
    imgc[mask] = [255, 192, 203]

    # plt.imshow(imgc)
    # plt.show()

    return imgc


# takes a gray-scale picture, offers two options for noise removal
# Notes: the method must be specified as 'uniform" or 'Gaussian'
def blurring(im, method):
    if method != 'uniform' and method != 'Gaussian':
        print ("Wrong Method!")
        return

    im1 = im[:, :, 0].copy()
    blurred = im[:, :, 0].copy()
    n, m = blurred.shape
    # uniform method
    if method == 'uniform':
        k = 5  # set our k value
        Filter = np.array([[1.0 / k ** 2] * k] * k)

        for i in range(int(k/2), n - int(k/2)):
            for j in range(int(k/2), m - int(k/2)):
                sub_matrix = im1[(i-(k-1)/2):((i+(k-1)/2)+1), (j-(k-1)/2):((j+(k-1)/2)+1)]
                # sub_matrix = np.array(sub_matrix, dtype='float')
                blurred[i, j] = np.sum(sub_matrix*Filter)

    # Gaussian method
    else:
        k = 5  # set our k value
        sigma = 1  # set our sigma value
        Filter = np.array([[0] * k] * k, dtype='float')
        for x in range(k):
            for y in range(k):
                Filter[x, y] = np.exp(-((x - (k - 1) * 0.5) ** 2 + (y - (k - 1) * 0.5) ** 2) / (2.0 * sigma ** 2))
        filter_sum = np.sum(Filter)
        Filter = Filter / filter_sum
        for i in range(int(k/2), n - int(k/2)):
            for j in range(int(k/2), m - int(k/2)):
                sub_matrix = im1[(i-(k-1)/2):((i+(k-1)/2)+1), (j-(k-1)/2):((j+(k-1)/2)+1)]
                # sub_matrix = np.array(sub_matrix, dtype='float')
                blurred[i, j] = np.sum(sub_matrix*Filter)

    blurred = [[[blurred[i, j]] * 3 for j in range(m)] for i in range(n)]
    # plt.imshow(blurred)
    # plt.show()
    return blurred


# takes a gray-scale image, detects edges with the option of horizontal, vertical or both
# Note: the method must be specified as "horizontal", "vertical", or "both"
def detect_edge(im, method):
    if method != "horizontal" and method != "vertical" and method != "both":
        print('Wrong Method!')
        return

    im1 = im[:, :, 0].copy()
    edged = im[:, :, 0].copy()
    n, m = edged.shape
    k = 3  # set our key value
    vertical_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    horizontal_filter = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # horizontal edge detecting
    if method == "horizontal":
        for i in range(int(k/2), n - int(k/2)):
            for j in range(int(k/2), m - int(k/2)):
                sub_matrix = im1[(i - (k - 1) / 2):((i + (k - 1) / 2) + 1), (j - (k - 1) / 2):((j + (k - 1) / 2) + 1)]
                Sh = np.sum(sub_matrix * horizontal_filter)
                edged[i, j] = (Sh+4.0)/8.0

    # vertical edge detecting
    elif method == "vertical":
        for i in range(int(k/2), n - int(k/2)):
            for j in range(int(k/2), m - int(k/2)):
                sub_matrix = im1[(i - (k - 1) / 2):((i + (k - 1) / 2) + 1), (j - (k - 1) / 2):((j + (k - 1) / 2) + 1)]
                Sv = np.sum(sub_matrix * vertical_filter)
                edged[i, j] = (Sv+4.0)/8.0

    # edge detecting both horizontal and vertical
    else:
        for i in range(int(k/2), n - int(k/2)):
            for j in range(int(k/2), m - int(k/2)):
                sub_matrix = im1[(i - (k - 1) / 2):((i + (k - 1) / 2) + 1), (j - (k - 1) / 2):((j + (k - 1) / 2) + 1)]
                Sh = np.sum(sub_matrix * horizontal_filter)
                Sv = np.sum(sub_matrix * vertical_filter)
                edged[i, j] = np.sqrt(Sv**2+Sh**2)/4.0

    edged = [[[edged[i, j]] * 3 for j in range(m)] for i in range(n)]
    # plt.imshow(edged)
    # plt.show()
    return edged

# test
'''def salt_pepper(im, ps=.1, pp=.1):
    im1 = im[:, :, 0].copy()
    n, m = im1.shape
    for i in range(n):
        for j in range(m):
            b = np.random.uniform()
            if b < ps:
                im1[i, j] = 1
            elif b > 1 - pp:
                im1[i, j] = 0
    noisy_im = [[[im1[i, j]] * 3 for j in range(m)] for i in range(n)]

    return noisy_im


def main():
    img = mpimg.imread('kitty-cat.jpg')

    heart(img)

    img = img / 255.0  # convert to float

    greyImg = img[:, :, 0] * 0.21 + img[:, :, 1] * 0.72 + img[:, :, 2] * 0.07
    greyImg = np.repeat(greyImg[:, :, np.newaxis], 3, axis=2)
    plt.imshow(greyImg, cmap='gray')
    plt.show()

    grey_salt_pepper = salt_pepper(greyImg)
    blurring(np.array(grey_salt_pepper), "uniform")
    blurring(np.array(grey_salt_pepper), "Gaussian")
    plt.imshow(grey_salt_pepper, cmap='gray')
    plt.show()

    detect_edge(greyImg, "horizontal")
    detect_edge(greyImg, "vertical")
    detect_edge(greyImg, "both")


if __name__ == '__main__':
    main()'''









