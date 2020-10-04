from PIL import Image
import time
import glob
import random

RANDOM = True

whitespaces = []

colorIndex = 0
colors = [(50, 10, 50), (200, 50, 180), (200, 50, 180), (120, 50, 10), (200, 20, 20), (50, 50, 50), (30, 30, 30)]

def get_pixel_value(image, coords):
  w, h = image.size
  if (coords[0] >= 0 and coords[0] < w and coords[1] >= 0 and coords[1] < h):
    return {"coords": coords, "color": image.getpixel(coords)}
  return None
      
def get_uncolored_around_cursor(image, x, y):
  uncolored = [0,0,0,0]
  # Up
  uncolored[0] = get_pixel_value(image, (x, y-1))
  # Down
  uncolored[1] = get_pixel_value(image, (x, y+1))
  # Left
  uncolored[2] = get_pixel_value(image, (x-1, y))
  # Right
  uncolored[3] = get_pixel_value(image, (x+1, y))
  return uncolored
  
def color_region(image, x, y, color):
  pixel_map = image.load()
  global colorIndex, colors
  
  # Color current pixel
  pixel_map[x,y] = color

  # Mark surrounding pixels to be colored + add to queue to search around surrounding pixels
  uncolored = get_uncolored_around_cursor(image, x, y)
  for pixel in uncolored:
    if pixel != None:
      if pixel['color'] == (255, 255, 255):
        whitespaces.append((pixel['coords'], color))
  

def color_image(image):
  global colorIndex, colors
  w,h = image.size
  for x in range(w):
    for y in range(h):
      if image.getpixel((x, y)) == (255, 255, 255):
        if RANDOM:
          color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
          color = colors[colorIndex]
        color_region(image, x, y, color)
        colorIndex = (colorIndex + 1) % len(colors)
        while len(whitespaces) != 0:
          current_pixel = whitespaces.pop()
          color_region(image, current_pixel[0][0], current_pixel[0][1], current_pixel[1])

def color_images():
  for filename in glob.glob('uncolored/*.bmp'):
    start_time = time.time()
    image = Image.open(filename).convert('RGB')
    name = filename.split('/')[1].split('.')[-2]
    if (glob.glob('colored/*.png').__contains__(f'colored/{name}.png') == False):
      color_image(image)
      image.save(f'colored/{name}.png')
      total_time = time.time() - start_time
      print(f'Created {filename} in {total_time} seconds!')
    else:
      print(f'{name} has already been colored!')

if __name__ == "__main__":
  color_images()
