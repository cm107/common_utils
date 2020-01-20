import cv2
import numpy as np

def cv_simple_image_viewer(img: np.ndarray, preview_width: int, window_name: str="Simple Image Viewer") -> bool:
    quit_flag = False

    # Window Declaration
    img_h, img_w = img.shape[:2]
    scale_factor = preview_width / img_w
    window_w, window_h = int(scale_factor * img_w), int(scale_factor * img_h)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, (window_w, window_h))
    cv2.imshow(window_name, img)
    quit_flag = False
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('n'):
            break
        elif key == ord('q'):
            quit_flag = True
            break
    cv2.destroyAllWindows()
    
    return quit_flag