import tensorflow as tf

# Step 2: Define a data pipeline using tf.data API
def parse_tfrecord_fn(example):
    # Define parsing function to convert TFRecord data to features and labels
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, feature_description)
    image = tf.io.decode_jpeg(example['image'], channels=3)
    label = example['label']
    return image, label

# Load TFRecord files using tf.data.TFRecordDataset
filenames = ['train.record']
raw_dataset = tf.data.TFRecordDataset(filenames)
parsed_dataset = raw_dataset.map(parse_tfrecord_fn)

# Step 3: Define your model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(None, None, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')  # Adjust the output size based on your problem
])

# Step 4: Compile your model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Step 5: Train your model
model.fit(parsed_dataset, epochs=5)
