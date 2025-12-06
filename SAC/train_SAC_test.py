import stable_baselines3 as sb3
from tqdm import tqdm, trange
import sys
sys.path.append('D:/project/RUNT')
sys.path.append('D:/project/RUNT/RUNT_env')
from utils.visualization import plot_rewards

def train_SAC(env, model, total_timesteps, verbose=1):
    '''Train SAC model.'''
    if model is None:
        model = sb3.SAC('MlpPolicy', env, verbose=verbose)
    model = model.learn(total_timesteps=total_timesteps)
    return model

def test_model(env, model, n_eval_episodes=3, render=True):
    '''Test the model.'''
    total_reward = 0.0
    for i in range(n_eval_episodes):
        done = False
        episode_reward = 0.0
        # 每次测试前重置环境
        obs, info = env.reset()
        for i in range(1000):
            if render:
                env.render()
            action, _states = model.predict(obs, deterministic=False)
            obs, reward, done, truncated, info = env.step(action)
            episode_reward += reward
            if done or truncated:
                break
        # print(f"Episode reward {episode_reward:.2f}")
        total_reward += episode_reward
    return total_reward/n_eval_episodes

def model_train_and_test(env, model, n_episode, episode_timesteps=1000):
    rewards = []
    ma_rewards = []
    for i in trange(n_episode):
        model.learn(total_timesteps=episode_timesteps)
        ep_reward = test_model(env, model, n_eval_episodes=10, render=True)
        rewards.append(ep_reward)
        ma_rewards.append((ma_rewards[-1]*0.95+ep_reward*0.05) if ma_rewards else ep_reward)
        with open('D:\project\RUNT\logs\log01.txt', 'a') as logs:
            logs.write(str(ep_reward)+', '+str(ma_rewards[-1])+'\n')
    plot_rewards(rewards=rewards, algorithm_name='SAC')
    return rewards, ma_rewards

if __name__ == '__main__':
    import RUNT_env.config as Cfg
    import RUNT_env.RUNT_Environment as RUNT_env
    cfg = Cfg.get_args()
    env = RUNT_env.RuntBoxEnv(cfg)
    model = sb3.SAC('MlpPolicy', env, verbose=1)
    model_train_and_test(env, model, 4000)
    import gymnasium as gym
    