import os
from tensorflow.keras import models, layers, optimizers, utils, losses, callbacks, initializers
import matplotlib.pyplot as plt

epochs = 150
batch_size = 32
patience = 10
learning_rate = 0.0001
num_classes = 17
model_path = 'checkpoints/model.keras'  

exists = os.path.exists(model_path) 

model = models.load_model(model_path) if exists else models.Sequential([
    layers.Resizing(128, 128),
    layers.Rescaling(1.0 / 255),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer=initializers.RandomNormal()),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer=initializers.RandomNormal()),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer=initializers.RandomNormal()),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu', kernel_initializer=initializers.RandomNormal()),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu', kernel_initializer=initializers.RandomNormal()),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax', kernel_initializer=initializers.RandomNormal())
])

if not exists:
    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss=losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )

train_dataset = utils.image_dataset_from_directory(
    "artistas",
    validation_split=0.2,
    subset="training",
    seed=123,
    shuffle=True,
    image_size=(128, 128),
    batch_size=batch_size
)

test_dataset = utils.image_dataset_from_directory(
    "artistas",
    validation_split=0.2,
    subset="validation",
    seed=123,
    shuffle=True,
    image_size=(128, 128),
    batch_size=batch_size
)

history = model.fit(
    train_dataset,
    epochs=epochs,
    validation_data=test_dataset,
    callbacks=[
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=patience,
            verbose=1,
            restore_best_weights=True
        ),
        callbacks.ModelCheckpoint(
            filepath=model_path,
            save_weights_only=False,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True
        )
    ]
)

train_accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
epochs = range(1, len(train_accuracy) + 1)

plt.plot(epochs, train_accuracy, 'b', label='Accuracy')
plt.plot(epochs, val_accuracy, 'r', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
