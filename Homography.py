import cv2
import numpy as np
from ultralytics import YOLO

  

# List to store clicked points
points = []

# Mouse callback function
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(image, f"{len(points)}", (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow("Select 4 Points (TL -> TR -> BR -> BL)", image)

# Load your frame or image
image = cv2.imread("/Users/nicovnexia/Desktop/images/BEV_test_4.jpeg")  #image path
clone = image.copy()

cv2.imshow("Select 4 Points (TL -> TR -> BR -> BL)", image)
cv2.setMouseCallback("Select 4 Points (TL -> TR -> BR -> BL)", click_event)

# Wait until 4 points are selected
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):  # Reset
        image = clone.copy()
        points = []
        cv2.imshow("Select 4 Points (TL -> TR -> BR -> BL)", image)
    elif key == ord("q") or len(points) == 4:
        break

cv2.destroyAllWindows()

if len(points) == 4:
    print("Selected points (in order):")
    for i, pt in enumerate(points):
        print(f"  Point {i + 1}: {pt}")
else:
    print("Less than 4 points selected.")

width = 300
height = 700

src_points = np.array(points, dtype=np.float32)
dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)


# Using getPerspectiveTransform
M = cv2.getPerspectiveTransform(src_points, dst_points)
warped_getPerspective = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))

cv2.imshow("Warped Image (getPerspectiveTransform)", warped_getPerspective)

# Using findHomography
H, _ = cv2.findHomography(src_points, dst_points)
warped_findHomography = cv2.warpPerspective(image, H, (width, height))
cv2.imshow("Warped Image (findHomography)", warped_findHomography)
cv2.waitKey(0)
cv2.destroyAllWindows()


  
## YOLO Segmentation


# Load your YOLOSeg model
model = YOLO('/Users/nicovnexia/Desktop/YOLOseg_best.pt')  # weights path

# Run inference
results = model(warped_findHomography, task='segment',conf=0.5)

# Visualize results
results[0].show() 
results[0].save(filename='bev_segmented.jpg') 