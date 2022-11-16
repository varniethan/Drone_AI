import numpy as np
import keras


class Augmenter():
    def __init__(self, p=0.5):
        self.p = p
    
    def __zoom(self, image):
        zoom = iaa.Affine(scale=(1, 1.3)) # Zoom by up to 130% in about centre
        image = zoom.augment_image(image)
        return image
    
    def __pan(self, image):
        pan = iaa.Affine(translate_percent= {"x" : (-0.1, 0.1), "y": (-0.1, 0.1)})
        image = pan.augment_image(image)
        return image
    
    def __brightness_random(self, image):
        brightness = iaa.Multiply((0.2, 1.2))
        image = brightness.augment_image(image)
        return image
    
    def __flip_random(self, image, yaw):
        image = cv2.flip(image, 1)
        steering_angle = -steering_angle # Steering angle needs to be flipped as well, since we are flipping horizontally
        return image, yaw
        
    def random_augment(self, image, yaw):
        image = mpimg.imread(image)
        if np.random.rand() < p and aug_pan == True:
            image = self.__pan(image)
        if np.random.rand() < p and aug_zoom == True:
            image = self.__zoom(image)
        if np.random.rand() < p and aug_brightness == True:
            image = self.__brightness_random(image)
        if np.random.rand() < p and aug_brightness == True:
            image, steering_angle = self.__flip_random(image, yaw)
        return image, yaw

    

def path_leaf(path):
    _, tail = ntpath.split(path)
    return tail

def load_training_data(data_dir, data):
    image_paths = []
    yaws = []

    side_cam_offset = 0.15
    
    for i in range(len(data)):
        row = data.iloc[i]
        centre_image_path, left_image_path, right_image_path = row[0], row[1], row[2]
        yaw = float(row[3])
        
        # Centre image
        image_paths.append(os.path.join(data_dir, centre_image_path.strip()))
        yaws.append(yaw)
        
        # Left image
        image_paths.append(os.path.join(data_dir, left_image_path.strip()))
        yaws.append(yaw + side_cam_offset)
        
        # Right image
        image_paths.append(os.path.join(data_dir, right_image_path.strip()))
        yaws.append(yaw - side_cam_offset)
        
    return np.asarray(image_paths), np.asarray(yaws)

columns = ["centre_image",
           "left_image",
           "right_image",
           "yaw",
           "speed",
           "throttle"]


data = pd.read_csv(os.path.join(data_dir, "piloting_log.csv"), names=columns)
print("[Data Reading]")
print("Number of total entries in \"" + data_dir + "\" dataset: " + str(len(data)))
print()
    
data["centre_image"] = data["centre_image"].apply(path_leaf)
data["left_image"] = data["left_image"].apply(path_leaf)
data["right_image"] = data["right_image"].apply(path_leaf)

# Data Balancing TODO

image_paths, yaws = load_training_data(data_dir + "/IMG", data)

X_train, X_valid, y_train, y_valid = train_test_split(image_paths,
                                                      yaws,
                                                      test_size=validation_proportion)
print("[Generating Labelled Data]")
print("Number of training datapoints: " + str(len(X_train)))
print("Number of validation datapoints: " + str(len(X_valid)))
print()

augmenter = Augmenter(p=p)

# Batch Generator
X_train_gen, y_train_gen = next(batch_generator(X_train, y_train, 1, 1))
X_valid_gen, y_valid_gen = next(batch_generator(X_valid, y_valid, 1, 0))

# Model TODO

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

plt.tight_layout()
plt.savefig("static/loss.png")

print()
print("Saved model as " + model_dir)
