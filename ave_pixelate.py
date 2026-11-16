import cv2
import numpy as np

def nearest_lower_power_of_2(x):
    return 2 ** (x.bit_length() - 1)

def pixelate_average_fast(input_path, output_path, N):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not load image.")

    h, w, _ = img.shape
    if h != w:
        raise ValueError("Input image must be square.")

    new_size = nearest_lower_power_of_2(w)
    img = cv2.resize(img, (new_size, new_size), interpolation=cv2.INTER_AREA)

    block_size = new_size // N

    # Reshape trick
    temp = img.reshape(N, block_size, N, block_size, 3)
    avg = temp.mean(axis=(1, 3), keepdims=True)

    # Broadcast back to full size
    pixelated = np.tile(avg, (1, block_size, 1, block_size, 1))
    pixelated = pixelated.reshape(new_size, new_size, 3).astype(np.uint8)

    cv2.imwrite(output_path, pixelated)
    print(f"Saved pixelated image to {output_path}")


# Example usage
if __name__ == "__main__":
    pixelate_average_fast(r"C:\Users\User\Pictures\c.jpg", r"C:\Users\User\Pictures\OUT.jpg", N=1024)