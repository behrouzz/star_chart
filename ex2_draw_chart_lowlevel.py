import core as sch
from hypatie.data import cities
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.now()
obs_loc = cities['strasbourg'][:2]

df = sch.visible_hipparcos(obs_loc, t)
df_show = df[df['Vmag']<4]
dc_const = sch.load_constellations()


fig, ax, df_show = sch.draw_chart(df, df_show, dc_const, alpha=0.3, figsize=(20,20))
plt.show()
