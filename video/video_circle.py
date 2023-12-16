'''
Generating video data with circles
'''
import numpy as np
import moviepy.editor as mp
import cv2

# generate growing circle
fps = 30
duration = 5
num_frames = fps * duration

images = []

for i in range(0, num_frames):
  width, height = 400
  prog = i / num_frames
  r0 = 10
  rf = width / 2
  r = r0 + round(prog * (rf - r0))
  
  frame = np.full((height, width, 3), 0, dtype=np.uint8)
  cv2.circle(frame, (r, r), r, (255, 255, 255), thickness=-1)

  images.append(frame)

clip = mp.ImageSequenceClip(images, fps=fps)
clip.write_videofile('clip_1.mp4')

# circle mask
def make_mask(r: int, num_frames: int, size: tuple[int, int], fg_color: tuple, bg_color: tuple) -> list[np.ndarray]:
  images = []

  for i in range(0, num_frames):
    width, height = size
    prog = i / num_frames
    d = 2 * r
    x = int(2 * prog * (width - d)) + r if i < num_frames // 2 else int(2 * (1 - prog) * (width - d)) + r
    y = int(prog * (height - d)) + r

    frame = np.full((height, width, 4), bg_color, dtype=np.uint8)
    cv2.circle(frame, (x, y), r, fg_color, thickness=-1)

    images.append(frame)
  
  return images

sky = mp.VideoFileClip('sky.mp4')
num_frames = int(sky.fps * sky.duration)

# overlay a moving circle
images = make_mask(50, num_frames, sky.size, (255,)*4, (0,)*4)
mask_clip = mp.ImageSequenceClip(images, fps=sky.fps)
composite = mp.CompositeVideoClip([sky, mask_clip], use_bgclip=True)
composite.write_videofile('clip_2.mp4')

# cut out a moving circle
images = make_mask(150, num_frames, sky.size, (0,)*4, (0, 0, 0, 255))
mask_clip = mp.ImageSequenceClip(images, fps=sky.fps)
composite = mp.CompositeVideoClip([sky, mask_clip], use_bgclip=True)
composite.write_videofile('clip_3.mp4')
