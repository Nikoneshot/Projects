#%%
import pandas as pd
import matplotlib.pyplot as plt

temp_vs_time = pd.read_csv('../temp_vs_time.csv', index_col=0, )
temp_vs_time.head()
temp_vs_time.plot(title='Matthew Aguilar')
plt.savefig('Matthew_Aguilar.pdf')
plt.show()
#%%
num1 = 10
num2 = 5
result = num1 + num2
if 20 <= result <= 30:
    result = 0
    print(result)
else:
    pass
print(result)
#%%
def dice_eval(arg1, arg2):
    if (arg1 + arg2 == 7) or (arg1 + arg2 == 11) :
        return ("Winner!")
    if (arg1 + arg2 == 2):
        return ("Craps!")
print(dice_eval(1,5))

#%%
product_id = "57649d7595"
if product_id.isdigit() == True:
    print(product_id)
#%%
