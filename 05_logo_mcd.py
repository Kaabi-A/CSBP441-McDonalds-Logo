import cv2
import numpy as np

# Canvas & colors
W, H = 800, 800
RED_BG = (0, 0, 222)        # McDonald's red (BGR)
GOLD_Y = (0, 204, 255)      # McDonald's yellow (BGR)
SHADOW = (20, 20, 20)       # subtle shadow
img = np.full((H, W, 3), RED_BG, np.uint8)

# Bézier helper
def qbez(p0, p1, p2, n=1600):
    t = np.linspace(0.0, 1.0, n).reshape(-1, 1)
    return ((1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2).astype(np.int32)

# Geometry — wider top + longer sides
BASELINE = 650
VALLEY_Y = 630              # longer middle leg (near baseline)
PEAK_Y   = 85               # LOWER number = higher peaks → longer side legs

LEFT_BASE_X, RIGHT_BASE_X = 240, 560
VALLEY_X = (LEFT_BASE_X + RIGHT_BASE_X) // 2
# wider top: peaks pushed outward
LEFT_PEAK_X, RIGHT_PEAK_X = 300, 500
THICKNESS = 40
R = THICKNESS // 2

# Curves
p0L, p1L, p2L = np.array([LEFT_BASE_X, BASELINE]), np.array([LEFT_PEAK_X, PEAK_Y]), np.array([VALLEY_X, VALLEY_Y])
p0R, p1R, p2R = np.array([VALLEY_X, VALLEY_Y]),   np.array([RIGHT_PEAK_X, PEAK_Y]), np.array([RIGHT_BASE_X, BASELINE])
curveL, curveR = qbez(p0L, p1L, p2L), qbez(p0R, p1R, p2R)

# Shadow
SHX, SHY = 3, 3
cv2.polylines(img, [curveL + (SHX, SHY)], False, SHADOW, THICKNESS, cv2.LINE_AA)
cv2.polylines(img, [curveR + (SHX, SHY)], False, SHADOW, THICKNESS, cv2.LINE_AA)
for (x, y) in [(LEFT_BASE_X+SHX, BASELINE+SHY),
               (RIGHT_BASE_X+SHX, BASELINE+SHY),
               (VALLEY_X+SHX, VALLEY_Y+SHY)]:
    cv2.circle(img, (x, y), R, SHADOW, -1, cv2.LINE_AA)

# Golden arches
cv2.polylines(img, [curveL], False, GOLD_Y, THICKNESS, cv2.LINE_AA)
cv2.polylines(img, [curveR], False, GOLD_Y, THICKNESS, cv2.LINE_AA)
for (x, y) in [(LEFT_BASE_X, BASELINE),
               (RIGHT_BASE_X, BASELINE),
               (VALLEY_X, VALLEY_Y)]:
    cv2.circle(img, (x, y), R, GOLD_Y, -1, cv2.LINE_AA)

# Flat feet
cv2.rectangle(img, (0, BASELINE+R), (W, H), RED_BG, -1)

# Show & save
cv2.imshow("McDonald's Logo - Wider Top, Longer Sides", img)
cv2.imwrite("mcdonalds_logo_wider_top_longer_sides.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
