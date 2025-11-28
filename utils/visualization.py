import matplotlib.pyplot as plt
import sys
import numpy as np
from utils.re_sm import exp_smooth

def reward_visualization(rewards, algorithm_name):
    algorithm_name = algorithm_name.upper()
    rewards_num = len(rewards)
    smoothed_rewards = exp_smooth(rewards)
    x=np.linspace(0, rewards_num, rewards_num)
    plt.subplot(2, 1, 1)
    plt.plot(x, rewards, label="Rewards",)
    plt.title(algorithm_name+"Rewards")
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.subplot(2, 1, 2)
    plt.plot(x, smoothed_rewards, color="blue")
    plt.title(algorithm_name+"Smoothed Rewards")
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.show()


def plot_rewards(rewards, algorithm_name):
    """
    Plot training curve with raw and smoothed rewards over episodes
    Args:
        rewards: list of episode rewards
        window_size: the size of the sliding window to smooth rewards
    """
    x = np.arange(1, len(rewards) + 1)
    y = np.array(rewards)
    y_smoothed = exp_smooth(rewards)

    fig, ax = plt.subplots()
    ax.plot(x, y, alpha=0.3, label='Reward')
    ax.plot(x, y_smoothed, color='red', label='Smoothed Reward')
    ax.legend()
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Reward')
    plt.suptitle(algorithm_name.upper()+' Training Curve')
    plt.show()
