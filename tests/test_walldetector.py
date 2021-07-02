import os

import cv2
import pytest

from ai.dataprovider.walldetector import WallDetector


test_values = [
    ('wall_detect_1.png', (0.22907654789308318, 0.2552554876615639, 0.3125303383945079, 0.32680203167437955,
                           0.3193227652434859, 0.3192461312494205, 0.38781647678133174, 0.329090275341073,
                           0.3125303383945079, 0.2552554876615639, 0.22907654789308318)),
    ('wall_detect_2.png', (0.24632572123677293, 0.24631717819755428, 0.24999275163403734, 0.27329096340376247,
                           0.3271131850785542, 0.3535424785077183, 0.3511642053810021, 0.3704099072201354,
                           0.336063476254805, 0.2744759019470864, 0.24632572123677293)),
]


@pytest.mark.parametrize("img,expected", test_values)
def test_calculate_distances(img, expected):
    wall_detector = WallDetector(700, 700, show_image=False)
    img = cv2.imread(os.path.abspath(f'tests/res/{img}'))
    result = wall_detector.calculate_distances(img)
    assert expected == result
