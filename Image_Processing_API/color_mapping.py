"""
Color Mapping Module
--------------------

This is for applying color maps to grayscale image data. It will be based on the pixel intensity values.

Functions:
- apply_color_map(frame, colormap='jet'): Applies a color map to a single image frame.
"""

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def apply_color_map(frame, colormap='jet'):
    """
        Applies a color map to a single image frame.

    """
    np_frame = np.array(frame, dtype=np.uint8)
    normalized_frame = np_frame / 255
    colored_frame = plt.get_cmap(colormap)(normalized_frame)
    plt.imshow(colored_frame, cmap=colormap)
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')