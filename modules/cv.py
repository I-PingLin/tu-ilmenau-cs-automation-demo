from typing import Tuple
import numpy as np
from PIL import Image
import cv2


def pil_to_cv(img: Image.Image) -> np.ndarray:
    arr = np.array(img.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def cv_to_pil(arr: np.ndarray) -> Image.Image:
    if len(arr.shape) == 2:
        return Image.fromarray(arr)
    rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def preprocess_image(
    img: Image.Image,
    width: int = 256,
    height: int = 256,
    blur_ksize: int = 3,
    grayscale: bool = False,
) -> np.ndarray:
    cv = pil_to_cv(img)
    cv = cv2.resize(cv, (width, height), interpolation=cv2.INTER_AREA)
    if blur_ksize and blur_ksize > 1 and blur_ksize % 2 == 1:
        cv = cv2.GaussianBlur(cv, (blur_ksize, blur_ksize), 0)
    if grayscale:
        cv = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
        return cv
    # return RGB for display
    return cv2.cvtColor(cv, cv2.COLOR_BGR2RGB)


def canny_edges(
    img: Image.Image,
    width: int = 256,
    height: int = 256,
    blur_ksize: int = 3,
    low_threshold: int = 100,
    high_threshold: int = 200,
) -> np.ndarray:
    cv = pil_to_cv(img)
    cv = cv2.resize(cv, (width, height), interpolation=cv2.INTER_AREA)
    if blur_ksize and blur_ksize > 1 and blur_ksize % 2 == 1:
        cv = cv2.GaussianBlur(cv, (blur_ksize, blur_ksize), 0)
    gray = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=low_threshold, threshold2=high_threshold)
    return edges
