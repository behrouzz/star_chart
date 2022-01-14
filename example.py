from core import draw_chart
from hypatie.data import cities
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Create sky charts every minute in one hour
t = datetime.now()
times = [t+timedelta(minutes=i) for i in range(60)]

obs_loc = cities['strasbourg'][:2]

for i in range(len(times)):
    fig, ax, df = draw_chart(obs_loc, times[i], mag_max=4, alpha=0.3)
    fig.savefig('pics/'+str(i).zfill(2)+'.jpg')
    plt.close(fig)
