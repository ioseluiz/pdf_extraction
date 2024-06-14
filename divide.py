import os
import random
import shutil

data_path = "data/"

# path to destination folders
train_folder = os.path.join(data_path, "train")
val_folder = os.path.join(data_path, "eval")
test_folder = os.path.join(data_path, "test")

# Define a list of image extensions
image_extensions  =['.jpg','.jpeg']

# Create a list of image filenames in "data_path"
img_list = [filename for filename in os.listdir(data_path) if os.path.splittext(filename)[-1] in image_extensions]

# Sets the random seed
random.seed(42)

# Shuffle the list of image filenames
random.shuffle(img_list)

# Determine the number of images for each set
train_size = int(len(img_list) * 0.70)
val_size = int(len(img_list) * 0.15)
test_size = int(len(img_list) * 0.15)

# Create destination folders if they don't exist
for folder_path in [train_folder, val_folder, test_folder]:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
# Copy image files to destination folders
for i, f in enumerate(img_list):
    if i < train_size:
        dest_folder = train_folder
    elif i < train_size + val_size:
        dest_folder = val_folder
    else:
        dest_folder = test_folder
    shutil.copy(os.path.join(data_path, f),os.path.join(dest_folder, f))
