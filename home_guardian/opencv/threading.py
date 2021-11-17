from __future__ import annotations

from threading import Lock, Thread
from typing import Any

import cv2.cv2 as cv2
from cv2.cv2 import VideoCapture
from cv2.mat_wrapper import Mat
from loguru import logger


class VideoCaptureThreading:
    """
    Class to capture video from a camera or a video file by Python threading.

    Inspired by https://github.com/gilbertfrancois/video-capture-async/blob/master/main/gfd/py/video/capture.py
    """

    def __init__(self, src: int = 0, width: int = 640, height: int = 480):
        """
        Initialize the video capture threading object.

        :param src: The source of the video.
        :param width: The width of the video.
        :param height: The height of the video.
        """
        self._thread: Thread = Thread(target=self._thread_loop, args=())
        self._src: int = src
        self._video_capture: VideoCapture = VideoCapture(self._src)
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width).set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # `_grabbed` is a boolean indicating if the frame is available or not
        self._grabbed, self._frame = self._video_capture.read()
        self._started = False
        self._read_lock = Lock()
        logger.warning("Initialized {}", self)

    def set(self, property_id: int, value: Any) -> VideoCaptureThreading:
        """
        Sets a property in the VideoCapture.

        :param property_id: The property id.
        :param value: The value of the property.
        :return: self
        """
        self._video_capture.set(property_id, value)
        return self

    def start(self) -> VideoCaptureThreading:
        """
        Start the thread to read frames from the video stream.

        :return: self
        """
        if self._started:
            logger.warning(
                "Threaded video capturing has already been started! Cannot be started again."
            )
            return self
        self._started = True
        self._thread.start()
        logger.debug("Started video capture thread. Thread: {}", self._thread)
        return self

    def _thread_loop(self) -> None:
        """
        [Private] Loop over frames from the video stream.
        """
        logger.warning("Started video capture loop. Thread: {}", self._thread)
        while self._started:
            grabbed, frame = self._video_capture.read()
            with self._read_lock:
                self._grabbed = grabbed
                self._frame = frame
        logger.warning("Stopped video capture loop. Thread: {}", self._thread)

    def read(self) -> tuple[bool, Mat]:
        """
        Read the frame from the video stream.

        :return: `grabbed` is a boolean indicating if the frame is available or not
        """
        with self._read_lock:
            grabbed = self._grabbed
            frame = self._frame.copy()
        return grabbed, frame

    def stop(self):
        """
        Stop the thread and release video capture object.
        """
        self._started = False
        self._thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        """
        Release video capture object
        """
        self._video_capture.release()
        logger.warning("Released {}", self)
