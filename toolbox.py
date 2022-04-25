import cv2

def rescale_frame( frame, pct_factor ):
    width = int(frame.shape[1] * (pct_factor / 100))
    height = int(frame.shape[0] * (pct_factor) / 100)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation = cv2.INTER_AREA)