import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(device)

# Load data
data = pd.read_csv('TSLA_stock_data_2023.csv')

# Provide the data
state=torch.randn(1000,7+7+7+30).to(device=device)
predict_price=torch.randn(1000,1).to(device=device)

# divide the data into training part and test part
state_train, state_test, predict_price_train,predict_price_test= train_test_split(state, predict_price,test_size=0.2, random_state=42)
train_loader = DataLoader(TensorDataset(state_train, predict_price_train), batch_size=5, shuffle=True)
test_loader = DataLoader(TensorDataset(state_test, predict_price_test), batch_size=1)

# construct NN
class NN(nn.Module):
    def __init__(self, n_observations):
        super(NN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)
    

# set some initail parameters 
LR = 1e-3
n_observations = len(state[0])

# value_net is your prediction function, take state as input and output is the prediction price
value_net = NN(n_observations).to(device)


# 'optimize'  is an easy package to do Gredient decent, 'Adam' is a method to let learing rate decay as step go.
optimizer = optim.Adam(value_net.parameters(), lr=LR)


# Optimazation function, it do one step of gredient decent, 
def optimize_model():
    for state, target in train_loader:
        current_value=value_net(state)                
        criterion = nn.SmoothL1Loss()
        loss=criterion(current_value,target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    for state, target in test_loader:
        with torch.no_grad():
            test_valur=value_net(state)                
            l_test=criterion(current_value,target)
    return loss.item(),l_test.item()

# training
epochs=10
for epoch in range(epochs):
    l_train,l_test=optimize_model()
    print(f'Epoch [{epoch+1}/{epochs}], L_train: {l_train},L_test: {l_test}')

