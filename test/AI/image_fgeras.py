# https://sabopy.com/py/scikit-image-30/
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray

image = plt.imread('./image/test_1.png')
fig, ax = plt.subplots(figsize=(5,5),dpi=100)
ax.imshow(image)
plt.savefig("./image/test_2.png",dpi=130)
plt.show()


image = rgb2gray(image)
img = img_as_float(image)

noise = np.ones_like(img) * 0.2 * (img.max() - img.min())
noise[np.random.random(size=noise.shape) > 0.5] *= -1

img_noise = img + noise
img_const = img + abs(noise)


def mse(x, y):
    return np.linalg.norm(x - y)
  
  
mse_none = mse(img, img)
ssim_none = ssim(img, img, data_range=img.max() - img.min())

mse_noise = mse(img, img_noise)
ssim_noise = ssim(img, img_noise,
                  data_range=img_noise.max() - img_noise.min())

mse_const = mse(img, img_const)
ssim_const = ssim(img, img_const,
                  data_range=img_const.max() - img_const.min())


fig = plt.figure(figsize=(8,3),dpi=150)
grid = ImageGrid(fig, 111,  
                 nrows_ncols=(1, 3),  
                 axes_pad=0.1)

label = 'MSE: {:.2f}, SSIM: {:.2f}'

grid[0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=1)
grid[0].set_xlabel(label.format(mse_none, ssim_none))
grid[0].set_title('Original image')

grid[1].imshow(img_noise, cmap=plt.cm.gray, vmin=0, vmax=1)
grid[1].set_xlabel(label.format(mse_noise, ssim_noise))
grid[1].set_title('Image with noise')

grid[2].imshow(img_const, cmap=plt.cm.gray, vmin=0, vmax=1)
grid[2].set_xlabel(label.format(mse_const, ssim_const))
grid[2].set_title('Image plus constant')
plt.savefig("ssim_zou.jpg", bbox_inches = 'tight', pad_inches = 0.05,dpi=130)
plt.show()