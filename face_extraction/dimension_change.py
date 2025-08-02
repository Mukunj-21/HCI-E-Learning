import os
import cv2
import numpy as np

input_dir = "cropped_faces_yolo"
output_dir = "cropped_faces_yolo_512_padded_4"
os.makedirs(output_dir, exist_ok=True)

def resize_with_padding(img, size=512, color=(0, 0, 0)):
    h, w = img.shape[:2]
    scale = size / max(h, w)
    resized_img = cv2.resize(img, (int(w * scale), int(h * scale)))

    h_padding = size - resized_img.shape[0]
    w_padding = size - resized_img.shape[1]

    top = h_padding // 2
    bottom = h_padding - top
    left = w_padding // 2
    right = w_padding - left

    padded_img = cv2.copyMakeBorder(resized_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return padded_img

# Process all images
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)

        if img is None:
            continue

        resized_padded = resize_with_padding(img, size=512)
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, resized_padded)

print("All images resized and saved to", output_dir)




# import os
# import cv2

# input_dir = "cropped_faces_yolo"
# output_dir = "cropped_faces_yolo_512"
# os.makedirs(output_dir, exist_ok=True)

# for filename in os.listdir(input_dir):
#     if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
#         img_path = os.path.join(input_dir, filename)
#         img = cv2.imread(img_path)

#         if img is None:
#             continue  # Skip unreadable images

#         resized_img = cv2.resize(img, (512, 512))
#         save_path = os.path.join(output_dir, filename)
#         cv2.imwrite(save_path, resized_img)

# print("All images resized to 512x512 and saved in", output_dir)

