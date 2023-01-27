import pandas as pd
import matplotlib.pyplot as plt

temp_vs_time = pd.read_csv('temp_vs_time.csv', index_col=0,)
temp_vs_time.head()
temp_vs_time.plot(title = 'Matthew Aguilar')
plt.savefig('Matthew_Aguilar.pdf')
plt.show()
#%%
