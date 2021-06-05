import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class linearQnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.hidden1 = nn.Linear(input_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.hidden1(x))
        x = self.output_layer(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.gamma = gamma
        self.lr = lr
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        """
        this function will train the neural network from the available parameters
        """
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)  # changing the format into tensor(for pytorch)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)  # if there is only one parameter
            action = torch.unsqueeze(action, 0)  # then change it to a different format
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        predict = self.model(state)  # get all the action/s that the network got
        target = predict.clone()
        for idx in range(len(game_over)):  # going through every action and saving in target a better version of it
            q_new = reward[idx]            # according to the equation q_new
            if not game_over[idx]:
                q_new = reward[idx] + self.gamma * torch.max(self.model(next_state))
            target[idx][torch.argmax(action).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, predict)  # changing the neural network to be more like the target
        loss.backward()

        self.optimizer.step()



