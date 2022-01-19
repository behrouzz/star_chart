import core as sch
from hypatie.data import cities
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.now()
obs_loc = cities['strasbourg'][:2]

# Base dataframe
df = sch.visible_hipparcos(obs_loc, t)

# DataFrame of stars that will be shown
df_show = df[df['Vmag']<4]

# Load constellation data
dc_const = sch.load_constellations()

# Show only Ursa Major and Cassiopeia constellations
dc_const = {'UMa': dc_const['UMa'],
            'Cas': dc_const['Cas']}


fig, ax, df_show = sch.draw_chart(df, df_show, dc_const, alpha=0.5)
plt.show()
