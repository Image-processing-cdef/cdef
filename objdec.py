# from ultralytics import YOLO
# import cv2
# import numpy as np
# from google.colab import files
# from IPython.display import display, Image
# import matplotlib.pyplot as plt
# from PIL import Image as PILImage
# import io

# print("upload image")
# uploaded = files.upload()

# image_path = list(uploaded.keys())[0]
# model = YOLO('yolov8m.pt')
# image = cv2.imread(image_path)
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# results = model(image)
# output_image = image_rgb.copy()
# detected_objects = {}
# object_frames = {}

# for result in results:
#     boxes = result.boxes
#     for box in boxes:
#         x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
#         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

#         confidence = float(box.conf[0])
#         class_id = int(box.cls[0])
#         class_name = model.names[class_id]

#         if confidence > 0.5:

#             cv2.rectangle(output_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             label = f'{class_name}: {confidence:.2f}'
#             cv2.putText(output_image, label, (x1, y1-10),
#                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             if class_name in detected_objects:
#                 detected_objects[class_name] += 1
#             else:
#                 detected_objects[class_name] = 1
#             frame = image_rgb[y1:y2, x1:x2]
#             if class_name not in object_frames:
#                 object_frames[class_name] = []
#             object_frames[class_name].append((frame, confidence))

# plt.figure(figsize=(15, 15))
# plt.imshow(output_image)
# plt.axis('off')
# plt.title('Detected Objects')
# plt.show()

# print("\nDetected Objects Summary:")
# for obj, count in detected_objects.items():
#     print(obj, ":", count, "instances")

# print("\nIndividual Object Frames:")
# for class_name, frames in object_frames.items():
#     print("\n" + class_name + " Detections:")

#     frames.sort(key=lambda x: x[1], reverse=True)

#     n_frames = len(frames)
#     if n_frames > 0:
#         fig, axes = plt.subplots(1, min(n_frames, 5), figsize=(15, 3))
#         if n_frames == 1:
#             axes = [axes]

#         for i, (frame, conf) in enumerate(frames[:5]):
#             axes[i].imshow(frame)
#             axes[i].axis('off')
#             axes[i].set_title(f'Conf: {conf:.2f}')

#         plt.suptitle(f'{class_name} Instances')
#         plt.show()
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage
import io
from appwrite.client import Client
from appwrite.services.storage import Storage

# Initialize YOLO model
model = YOLO('yolov8m.pt')

# Replace with your Appwrite project details
APPWRITE_ENDPOINT = 'https://cloud.appwrite.io/v1'
APPWRITE_PROJECT_ID = '67176323003bf16cbd3f'
APPWRITE_API_KEY = 'standard_27d81950ea80941e3161da22e8b4b66fd794d919dfe962a75894d05e2e05fe4338b56652d503ec5caa6dfd7e99ffcd55051b33a34be9ee1c90f6b5d6c5f1e5cb040e9fe3e5817eb9dd83afa8d00f89f55f3c6a6e667cb3c0ef3a78f642a96c42265d36ee5118f6069fcf0dccfa02ecea0c5a7780cf20b35aa0cd65983183cdc3'
BUCKET_ID = '6720d05c00113044676a'
FILE_ID = '67213398000058c39dd6'

# Initialize Appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

# Initialize Appwrite storage service
storage = Storage(client)

# Download the file from Appwrite bucket
print("Downloading image from Appwrite storage...")
file_response = storage.get_file_download(BUCKET_ID, FILE_ID)

# Convert response content to OpenCV image format
image = PILImage.open(io.BytesIO(file_response))
image = np.array(image)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run YOLO model on the image
results = model(image)
output_image = image_rgb.copy()
detected_objects = {}
object_frames = {}

for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if confidence > 0.5:
            # Draw bounding box and label on the image
            cv2.rectangle(output_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'{class_name}: {confidence:.2f}'
            cv2.putText(output_image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Count and store each detected object
            if class_name in detected_objects:
                detected_objects[class_name] += 1
            else:
                detected_objects[class_name] = 1

            # Crop the object frame and store
            frame = image_rgb[y1:y2, x1:x2]
            if class_name not in object_frames:
                object_frames[class_name] = []
            object_frames[class_name].append((frame, confidence))

# Display the output image with detections
plt.figure(figsize=(15, 15))
plt.imshow(output_image)
plt.axis('off')
plt.title('Detected Objects')
plt.show()

# Print detected object summary
print("\nDetected Objects Summary:")
for obj, count in detected_objects.items():
    print(obj, ":", count, "instances")

# Show individual object frames with confidence
print("\nIndividual Object Frames:")
for class_name, frames in object_frames.items():
    print("\n" + class_name + " Detections:")

    frames.sort(key=lambda x: x[1], reverse=True)

    n_frames = len(frames)
    if n_frames > 0:
        fig, axes = plt.subplots(1, min(n_frames, 5), figsize=(15, 3))
        if n_frames == 1:
            axes = [axes]

        for i, (frame, conf) in enumerate(frames[:5]):
            axes[i].imshow(frame)
            axes[i].axis('off')
            axes[i].set_title(f'Conf: {conf:.2f}')

        plt.suptitle(f'{class_name} Instances')
        plt.show()
