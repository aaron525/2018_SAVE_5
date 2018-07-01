import os  
from tqdm import tqdm
import cv2
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = './training_set'
TEST_DIR = './test_set'
IMG_SIZE = 50
IGNORE_FILES = ['.DS_Store']


def create_train_test_dir():
    counter=1
    _train_dir = [ "./training_data/cats", "./training_data/dogs" ]
    for _dir in _train_dir:
        if not os.path.exists(_dir):
            os.system('mkdir -p %s' % (_dir))
            print('%s directory is created!' % (_dir))
    for root, dirs, imgs in os.walk(TRAIN_DIR):
        for img in imgs:
            if img in IGNORE_FILES: continue
            word_label = img.split('.')[-3]
            if word_label == 'cat':lable="cats"
            elif word_label == 'dog':lable="dogs"
            path = os.path.join(root,img)
            img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
            cv2.imwrite("./training_data/"+lable+'/'+str(counter)+'.jpg',img)
            counter += 1

def process_val_data():
    counter=1
    _test_dir = [ "./testing_data/cats", "./testing_data/dogs" ]
    for _dir in _test_dir:
        if not os.path.exists(_dir):
            os.system('mkdir -p %s' % (_dir))
            print('%s directory is created!' % (_dir))
    for root, dirs, imgs in os.walk(TEST_DIR):
        for img in imgs:
            if img in IGNORE_FILES: continue
            word_label = img.split('.')[-3]
            if word_label == 'cat': lable="cats"
            elif word_label == 'dog': lable="dogs"
            path = os.path.join(root,img)
            img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
            cv2.imwrite("./testing_data/"+lable+'/'+str(counter)+'.jpg',img)
            counter += 1

def model_tain_evaluate():

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape = (50, 50, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(32, (3, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Flatten())
    model.add(Dense(units = 128, activation = 'relu'))
    model.add(Dense(units = 1, activation = 'sigmoid'))

    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    train_datagen = ImageDataGenerator(rescale = 1./255, \
                                       shear_range = 0.2, \
                                       zoom_range = 0.2, \
                                       horizontal_flip = True)
    training_set = train_datagen.flow_from_directory('training_data', \
                                                      target_size = (50, 50), \
                                                      batch_size = 32, \
                                                      class_mode = 'binary')
    test_datagen = ImageDataGenerator(rescale=1./255)
    validation_generator = test_datagen.flow_from_directory('testing_data', \
                                                             target_size=(50, 50), \
                                                             batch_size=32, \
                                                             class_mode='binary')
    model.fit_generator(training_set, \
                        steps_per_epoch = 8000, \
                        epochs = 5, \
                        validation_data = validation_generator, \
                        validation_steps = 2000)

    model_json = model.to_json()
    with open("./model.json","w") as json_file:
      json_file.write(model_json)

    model.save_weights("./model.h5")
    print("saved model..! ready to go.")

if __name__ == "__main__":
    create_train_test_dir()
    process_val_data()
    model_tain_evaluate()


