import cv2.cv2 as cv2


def capture_edge_video() -> None:
    """
    Capture video from camera and transform it into edge video.
    """
    cap = cv2.VideoCapture(0)
    while True:
        # reads frames from a camera
        ret, frame = cap.read()
        # Display an original image
        cv2.imshow("Original", frame)
        # discovers edges in the input image image and
        # marks them in the output map edges
        edges = cv2.Canny(frame, 100, 200, True)
        # Display edges in a frame
        cv2.imshow("Edges", edges)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
