import av
import cv2


camera = "rtsp://admin:3m3m3m3m@192.168.1.64:554/onvif2"

container = av.open(camera)

stream = next(s for s in container.streams if s.type == "video")

for frame in container.decode(stream):

    img = frame.to_ndarray(format="bgr24")

    cv2.imshow("Camera RTSP (PyAV)", img)

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cv2.destroyAllWindows() 