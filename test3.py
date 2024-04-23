import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import pandas as pd
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
data = pd.read_csv('TSLA_stock_data_2023.csv')
state=[]
predictprice=[]
timeinclude=21 # how many time of past you want to include to predict
for t in range(len(data)-timeinclude-7):
    state_t=data.iloc[t:t+timeinclude,1:6].values # the state variable you need
    state_t=state_t.reshape(1,-1).squeeze() # squeeze data into 1 dimension
    predictprice_t=data['Close'][t+timeinclude+6]
    state.append(state_t)
    predictprice.append(predictprice_t)
# provide your selfdata
state=np.array(state)
predictprice=np.array(predictprice)
state=torch.tensor(state).to(device) # This is your x
predictprice=torch.tensor(predictprice).to(device) # This is your y, you will use x to predict y
print(predictprice[0])
print(state[0])