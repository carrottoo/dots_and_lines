import jax.numpy as np
import matplotlib.pyplot as plt
import jax
import jax.scipy as jsp

jax.config.update("jax_enable_x64", True)
import scipy
width = 1000
height = 1000
np.zeros((width, height))
key = jax.random.PRNGKey(0)

def temperature_to_rgb(temperature):
    temperature /= 100.0
    if temperature <= 66:
        red = 255
    else:
        red = temperature - 60.0
        red = 329.698727446 * (red ** -0.1332047592)
        red = np.maximum(0, np.minimum(255, red))

    if temperature <= 66:
        green = temperature
        green = 99.4708025861 * np.log(green) - 161.1195681661
        green = np.maximum(0, np.minimum(255, green))
    else:
        green = temperature - 60.0
        green = 288.1221695283 * (green ** -0.0755148492)
        green = np.maximum(0, np.minimum(255, green))

    if temperature >= 66:
        blue = 255
    elif temperature <= 19:
        blue = 0
    else:
        blue = temperature - 10.0
        blue = 138.5177312231 * np.log(blue) - 305.0447927307
        blue = np.maximum(0, np.minimum(255, blue))

    return np.array([red,green,blue])

def ball(x, y, center_x, center_y, radius):
  dx = x - center_x
  dy = y - center_y
  return (np.sqrt(dx*dx + dy*dy) < radius) * 0.1



def star(x, y, center_x, center_y, inv_radius, color):
  dx = x - center_x
  dy = y - center_y
  brightness = 1/(0.01 + np.sqrt(dx*dx + dy*dy) * inv_radius)**50
  return brightness[..., None] * temperature_to_rgb(color)

