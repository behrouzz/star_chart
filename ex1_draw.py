from core import draw
from hypatie.data import cities
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.now()
obs_loc = cities['strasbourg'][:2]

fig, ax, df = draw(obs_loc, t, mag_max=4, alpha=0.3, figsize=(12,12))
plt.show()
