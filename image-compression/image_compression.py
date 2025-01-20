from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

PATH = input("Enter the path of the iamge: ").replace("\\", "\\\\")
original_image_size = 0

def get_rgb_values(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    data = list(image.getdata())
    return ([row[0] for row in data], [row[1] for row in data], [row[2] for row in data])

def get_image_size(image_path):
    image = Image.open(image_path)
    return image.size

size = get_image_size(PATH)

def reshape_into_image(y, x, r, g, b):
    data = np.column_stack([r, g, b])
    return np.reshape(data, (x, y, 3)).astype('int')

def pad_to_square(matrix):
    rows, cols = matrix.shape
    size = max(rows, cols) 
    square_matrix = np.zeros((size, size))
    square_matrix[:rows, :cols] = matrix  
    return square_matrix

def SVD_decomp(A):
    return np.linalg.svd(A, full_matrices= False)

def PCA_via_SVD_decomp(A, k, half_precision = False): 
    u, e, Vt = A

    diag_e = np.diag(e[:k])
    comp_u = u[:,:k]
    comp_Vt = Vt[:k,:]

    if half_precision:
        comp_u = comp_u.astype(np.float16)
        comp_Vt = comp_Vt.astype(np.float16)

    original_size = u.size + len(e) + Vt.size
    comp_size = comp_u.size + k + comp_Vt.size
    if half_precision:
        comp_size = comp_size / (4/3)

    return (comp_u @ diag_e @ comp_Vt).flatten(), (original_size, comp_size)

def run_test(A_matrices, compression_factor, specific_k = False, half_precision = False):
    r_matrix, g_matrix, b_matrix = A_matrices
    initial_k = A_matrices[0][1].shape[0]
    k = int(compression_factor * initial_k)
    if specific_k:
        k = specific_k

    pca =  PCA_via_SVD_decomp(r_matrix, k, half_precision), PCA_via_SVD_decomp(g_matrix, k, half_precision), PCA_via_SVD_decomp(b_matrix, k, half_precision)

    new_r, new_g, new_b = [pca[n][0] for n in range(len(pca))]
    compression_info = [pca[n][1] for n in range(len(pca))][0]

    comp_size_bytes = ((3 * compression_info[1]) * 4)
    comp_size_mb = comp_size_bytes / 1000000

    if k == initial_k:
        global original_image_size
        original_image_size = round(comp_size_mb, 2)

    if half_precision:
        return (reshape_into_image(size[0], size[1], new_r, new_g, new_b), f'{k}/{initial_k} PCs ({round(100 * k/initial_k, 2)}%) + half precision')
    return (reshape_into_image(size[0], size[1], new_r, new_g, new_b), f'{k}/{initial_k} PCs ({round(100 * k/initial_k, 2)}%)')

def show(data, titles):
    fig, axes = plt.subplots(2, 4)
    for ax, img, title in zip(axes.ravel(), data, titles):
        ax.imshow(img)
        ax.set_title(title)
        ax.axis('off') 
    plt.tight_layout()
    plt.show()

def main():
    r, g, b = get_rgb_values(PATH)
    r_matrix, g_matrix, b_matrix = map(lambda values: np.reshape(values, size), (r, g, b))
    a = SVD_decomp(r_matrix), SVD_decomp(g_matrix), SVD_decomp(b_matrix)

    k_percents = [1, 0.2, 0.1, 0.05, 0.05, 0.01, 0.005, 1]
    k_amounts = [False, False, False, False, False, False, False, 1]

    data = (
        run_test(a, 1, k_amounts[0]),
        run_test(a, k_percents[1], k_amounts[1]),
        run_test(a, k_percents[2], k_amounts[2]),
        run_test(a, k_percents[3], k_amounts[3]),
        run_test(a, k_percents[4], k_amounts[4], half_precision = True),
        run_test(a, k_percents[5], k_amounts[5]),
        run_test(a, k_percents[6], k_amounts[6]),
        run_test(a, k_percents[7], k_amounts[7])
    )

    data, titles = [d[0] for d in data], [d[1] for d in data]
    titles[0] = 'No Compression ' + f'{original_image_size}MB'
    show(data, titles)

if __name__ == '__main__':
    main()