'''
Generating video data with squares
'''
import numpy as np
import moviepy.editor as mp
import colorsys

def angle_to_rgb(angle: float) -> tuple:
  return tuple(int(255 * x) for x in colorsys.hsv_to_rgb(angle, 1, 1))

# generate color changing video with a square that moves
images = []
fps = 30 # Framerate
duration = 5 # Number of seconds
num_frames = fps * duration # Number of frames to generate

for i in range(0, num_frames):
  width = 400
  height = 500
  square = 100

  prog = i / num_frames
  color = angle_to_rgb(prog)
  frame = np.full((height, width, 3), color, dtype=np.uint8)

  x = int(2 * prog * (width - square)) if i < num_frames // 2 else int(2 * (1 - prog) * (width - square))
  y = int(prog * (height - square))

  stroke = 10
  frame[y:y + square, x:x + square] = 255
  frame[y + stroke:y + square - stroke, x + stroke:x + square - stroke] = color

  images.append(frame)

clip = mp.ImageSequenceClip(images, fps=fps)
clip.write_videofile('clip.mp4')

# add a mask to the previous video
mask_frame = np.full((height, width, 4), [0, 0, 0, 255], dtype=np.uint8)
pad = 100 # Black border width
mask_frame[pad:height - pad, pad:width - pad] = 0

mask_clip = mp.ImageClip(mask_frame, duration=duration)

composite = mp.CompositeVideoClip([clip, mask_clip], use_bgclip=True)
composite.write_videofile('composite.mp4')