**Author:** [Behrouz Safari](https://behrouzz.github.io/)<br/>
**Website:** [AstroDataScience.Net](https://astrodatascience.net/)<br/>

# Star Chart
Creating star charts with python


## Example

```python
from core import draw
from hypatie.data import cities
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.now()
obs_loc = cities['strasbourg'][:2]

fig, ax, df = draw(obs_loc, t, mag_max=4, alpha=0.3)
plt.show()
```
