from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.layers import Input, Dense, Flatten
from keras.optimizers import Adam
from keras.datasets import cifar10


def fine_tuned_model(num_classes, shape):
    initial_model = ResNet50(include_top=False, input_shape=shape)
    x = Flatten()(initial_model.output)
    x = Dense(num_classes, activation='softmax')(x)
    model = Model(initial_model.input, x)

    # Train only higher layers to avoid overfitting
    for layer in model.layers[:15]:
        layer.trainable = False

    # Learning rate is changed to 0.001
    adam = Adam(lr=1e-3, decay=1e-6)
    model.compile(optimizer=adam, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model


if __name__ == '__main__':
    img_rows, img_cols = 32, 32
    channels = 3
    num_classes = 10
    batch_size = 16
    epochs = 10

    # Replace with your own dataset.
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    y_train = y_train.flatten()
    y_test = y_test.flatten()

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # 10 classes because dataset is Cifar-10
    model = fine_tuned_model(10, (img_rows, img_cols, channels))

    # Fit model on the training and testing datasets
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              shuffle=True,
              verbose=1,
              validation_data=(x_test, y_test)
              )

