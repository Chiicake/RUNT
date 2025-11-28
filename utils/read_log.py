'''
This file is used to read the logs file in the logs folder and return the rewards and ma_rewards list in the logs.
'''

def read_log(file_name='ppo_exp1_logs.txt', num_of_logs = 3000):
    '''
    read the logs file in the logs folder and return the rewards and ma_rewards list in the logs.
    '''
    rewards = []
    ma_rewards = []
    cnt = 0
    with open(file_name, 'r') as logs:
        for lines in logs:
            try:
                num_list = lines.split(', ')
                rewards.append(float(num_list[0]))
                ma_rewards.append(float(num_list[1]))
            except:
                continue
            else:
                cnt += 1
                if cnt == num_of_logs:
                    break
    return rewards, ma_rewards

if __name__ == '__main__':
    from visualization import reward_visualization, plot_rewards
    algorithm_name = 'a2c'
    device_number = '5'
    MEC_computation_capacity = '6000'
    rewards, ma_rewards = read_log(file_name=algorithm_name+'_exp_'+
                                    device_number+'_'+MEC_computation_capacity+'_logs.txt', num_of_logs=1500)
    max_reward = max(rewards)
    print(algorithm_name+'_exp_'+device_number+'_'+MEC_computation_capacity+' best reward:', max_reward)
    #reward_visualization(rewards=rewards, algorithm_name=algorithm_name)
    plot_rewards(rewards=rewards, algorithm_name=algorithm_name)