from RUNT_env.config import get_args

def get_args_with_params(algorithm=None, target_episode=None, current_episode=None, status=None,
                         task_size_average=None, task_comsumption_average=None, task_time_average=None,
                         task_arrival_rate=None, n_UE=None, UE_computation_capacity=None,
                         MEC_computation_capacity=None, seed=None, learning_rate=None,
                         batch_size=None, gamma=None):
    """
    get system configuration with custom parameters
    For parameters that overlap with the original get_args, use the provided values;
    for others, use default values from the original get_args
    """
    # First get default args from original function
    default_args = get_args()

    # Create a dictionary to store the final args
    final_args = default_args.copy()

    # Update with provided parameters that overlap with original args
    if MEC_computation_capacity is not None:
        final_args['MEC_computation_capacity'] = MEC_computation_capacity
    if task_size_average is not None:
        final_args['task_size_average'] = task_size_average
    if task_comsumption_average is not None:
        final_args['task_comsumption_average'] = task_comsumption_average
    if task_time_average is not None:
        final_args['task_time_average'] = task_time_average
    if task_arrival_rate is not None:
        final_args['task_arrival_rate'] = task_arrival_rate
    if n_UE is not None:
        final_args['n_UE'] = n_UE
    if UE_computation_capacity is not None:
        final_args['UE_computation_capacity'] = UE_computation_capacity
    if seed is not None:
        final_args['seed'] = seed

    return final_args
