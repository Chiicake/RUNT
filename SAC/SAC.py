from stable_baselines3 import SAC
import sys
import numpy as np
sys.path.append('D:/project/RUNT')

def SAC_test(env, model_name, seed=0):
    '''Test the model.'''
    model = SAC.load('models/'+model_name)
    np.random.seed(seed)
    obs = env.reset()
    done = False
    total_reward = 0
    for i in range(1000):
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward -= reward
    #print(obs)
    return total_reward


def make_SAC_model(env, model_name="sac_my_env"):
    model = SAC("MlpPolicy", env, verbose=1, learning_rate=0.00003, tensorboard_log='./SAC/')
    model.save('models/'+model_name)



if __name__ == "__main__":
    import torch
    s = np.array((1, 4))
    print(s)
    s = torch.tensor(s, dtype=torch.float32)
    print(s)