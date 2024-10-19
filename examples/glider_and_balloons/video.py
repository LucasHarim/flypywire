import cv2
from flypywire import unityapi as unity

if __name__ == '__main__':

    cam = unity.Camera()
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can try 'MJPG', 'XVID', etc.
    out = cv2.VideoWriter('output_glider.avi', fourcc, 20.0, (640, 480))

    while True:
        
        if cam.is_connected:
            frame = cam.get_image()
            out.write(frame)
            cv2.imshow('Camera', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
    cv2.destroyAllWindows()
    out.release()


            
