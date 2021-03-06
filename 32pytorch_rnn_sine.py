
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

N = 1000
series = np.sin(0.1*np.arange(N))
plt.plot(series);

X = []
Y = []
T = 10

for t in range(len(series) - T):
    x = series[t:T+t]
    X.append(x)
    y = series[t+T]
    Y.append(y)

X = np.array(X).reshape(-1, T, 1)
Y = np.array(Y).reshape(-1, 1)

class RNN(nn.Module):
    def __init__(self, input_feature, num_layers, hidden_features, out_feature):
        super(RNN, self).__init__()
        # self.batch_size = N
        # self.time_step = T
        self.D = input_feature
        self.L = num_layers
        self. M = hidden_features
        self.K = out_feature

        self.rnn = nn.RNN(
            input_size = self.D,
            hidden_size = self.M,
            num_layers = self.L,
            nonlinearity = 'relu',
            batch_first = True
        )

        self.fc = nn.Linear(self.M, self.K)

    def forward(self, X):
        h0 = torch.zeros(self.L, X.size(0), self.M).to(device)
        out, _ = self.rnn(X, h0)
        out = self.fc(out[:, -1, :])
        return out

model = RNN(input_feature = 1,
            num_layers = 2,
            hidden_features = 5,
            out_feature = 1
            )

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
model.to(device)
# print(device)

optimizer = torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()

X_train = torch.from_numpy(X[:N//2].astype(np.float32)).to(device)
X_test = torch.from_numpy(X[N//2:].astype(np.float32)).to(device)
Y_train = torch.from_numpy(Y[:N//2].astype(np.float32)).to(device)
Y_test = torch.from_numpy(Y[N//2:].astype(np.float32)).to(device)

X.shape

X_train.shape

X_train[1]

def traning(X_train, X_test, Y_train, Y_test, criterion, optimizer, device, model, epochs):
    train_losses = []
    test_losses = []
    for i in range(epochs):
        optimizer.zero_grad()
        output = model(X_train)
        train_loss = criterion(output, Y_train)
        train_losses.append(train_loss.item())
        train_loss.backward()
        optimizer.step()
        
        
        output = model(X_test)
        test_loss = criterion(output, Y_test)
        test_losses.append(test_loss.item())

        if i%5 == 0:
            print(f'Train Loss: {train_loss.item()}, Test Loss: {test_loss.item()}')
    return train_losses, test_losses

train_losses, test_losses = traning(X_train, X_test, Y_train, Y_test, criterion, optimizer, device, model, epochs=1000)

plt.plot(train_losses, label = 'Train Loss')
plt.plot(test_losses, label = 'Test Loss')
plt.legend();

# Wrong Forcast

validation_targets = Y[N//2:]
validation_prediction = []
i = 0

while len(validation_prediction)<len(validation_targets):
    inputs = X_test[i].reshape(1, T, 1)
    output = model(inputs)[0,0].item()
    validation_prediction.append(output)
    i += 1

plt.plot(validation_prediction, label='Predcition')
plt.plot(validation_targets, label='Targets')
plt.legend();

X_test[0].view(T)

# Correct Forcast

validation_target = Y[N//2:]
validation_predictions = []

last_x = X_test[0].view(T)

while len(validation_prediction) < len(validation_target):
    input = last_x.reshape(1, T, 1)
    output = model(input)
    validation_prediction.append(output[0, 0].item())

    last_x = torch.cat((last_x[1:], output[0]))

plt.plot(validation_prediction, label='Predcition')
plt.plot(validation_targets, label='Targets')
plt.legend();
