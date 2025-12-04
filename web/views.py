from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from RUNT_env.RUNT_Environment import RuntBoxEnv
from SAC.make_config import get_args_with_params
from SAC.train_SAC_test import test_model
from .models import User
from .model.rl_model import RLModel
from .model.train_data import TrainData
import os
import decimal
import threading
import stable_baselines3 as sb3
# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # 从数据库中查询用户
            user = User.objects.get(username=username)
            # 验证密码
            if user.check_password(password):
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '用户名或密码错误'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '用户名或密码错误'})
    else:
        return JsonResponse({'status': 'error', 'message': '仅支持POST请求'})

@csrf_exempt
def train(request):
    if request.method == 'POST':
        try:
            # 获取请求参数
            algorithm = request.POST.get('algorithm')
            target_episode = request.POST.get('target_episode')
            task_size_average = request.POST.get('task_size_average')
            task_comsumption_average = request.POST.get('task_comsumption_average')
            task_time_average = request.POST.get('task_time_average')
            task_arrival_rate = request.POST.get('task_arrival_rate')
            n_UE = request.POST.get('n_UE')
            UE_computation_capacity = request.POST.get('UE_computation_capacity')
            MEC_computation_capacity = request.POST.get('MEC_computation_capacity')
            seed = request.POST.get('seed')
            learning_rate = request.POST.get('learning_rate')
            batch_size = request.POST.get('batch_size')
            gamma = request.POST.get('gamma')
            
            # 参数验证和类型转换
            if not algorithm:
                return JsonResponse({'status': 'error', 'message': 'algorithm参数不能为空'}, status=400)
            
            if not target_episode:
                return JsonResponse({'status': 'error', 'message': 'target_episode参数不能为空'}, status=400)
            
            # 验证并转换数值型参数
            try:
                target_episode = int(target_episode)
                if target_episode < 0:
                    return JsonResponse({'status': 'error', 'message': 'target_episode必须为非负整数'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'target_episode必须为整数'}, status=400)
            

            
            # 处理Decimal类型参数
            def parse_decimal(value, max_digits, decimal_places):
                if value is None:
                    return None
                try:
                    # 将字符串转换为Decimal
                    dec_value = decimal.Decimal(value)
                    # 格式化保留指定小数位数
                    formatted = round(dec_value, decimal_places)
                    # 检查总位数是否超过限制
                    if formatted.as_tuple().digits and len(formatted.as_tuple().digits) > max_digits:
                        raise ValueError(f"数值位数超过限制，最多{max_digits}位")
                    return formatted
                except decimal.InvalidOperation:
                    raise ValueError("必须为有效的数值")
            
            try:
                task_size_average = parse_decimal(task_size_average, 10, 4)
                task_comsumption_average = parse_decimal(task_comsumption_average, 10, 4)
                task_time_average = parse_decimal(task_time_average, 10, 4)
                task_arrival_rate = parse_decimal(task_arrival_rate, 8, 4)
                UE_computation_capacity = parse_decimal(UE_computation_capacity, 10, 2)
                MEC_computation_capacity = parse_decimal(MEC_computation_capacity, 12, 2)
                learning_rate = parse_decimal(learning_rate, 8, 6)
                gamma = parse_decimal(gamma, 8, 6)
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'数值参数格式错误: {str(e)}'}, status=400)
            
            # 处理非负整数参数
            def parse_positive_int(value):
                if value is None:
                    return None
                try:
                    int_value = int(value)
                    if int_value < 0:
                        raise ValueError("必须为非负整数")
                    return int_value
                except ValueError:
                    raise ValueError("必须为整数")
            
            try:
                n_UE = parse_positive_int(n_UE)
                seed = parse_positive_int(seed)
                batch_size = parse_positive_int(batch_size)
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'整数参数格式错误: {str(e)}'}, status=400)
            
            # 使用事务确保数据库操作和文件创建的原子性
            with transaction.atomic():
                # 创建RLModel实例
                rl_model = RLModel(
                    algorithm=algorithm,
                    target_episode=target_episode,
                    current_episode=0,
                    status=0,
                    task_size_average=task_size_average,
                    task_comsumption_average=task_comsumption_average,
                    task_time_average=task_time_average,
                    task_arrival_rate=task_arrival_rate,
                    n_UE=n_UE,
                    UE_computation_capacity=UE_computation_capacity,
                    MEC_computation_capacity=MEC_computation_capacity,
                    seed=seed,
                    learning_rate=learning_rate,
                    batch_size=batch_size,
                    gamma=gamma
                )
                
                # 保存到数据库，获取自增id
                rl_model.save()

            # 异步训练
            def async_train(model_id, algo, target_ep, task_size_avg, task_cons_avg, task_time_avg, task_arr_rate, 
                          n_ue, ue_comp_cap, mec_comp_cap, seed_val, lr, batch_sz, gamma_val):
                try:
                    # 创建一个日志文件
                    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../models/train_log/train_log_{model_id}.txt')
                    # 写入开始信息
                    with open(log_file, 'w') as f:
                        f.write(f'训练开始，model_id: {model_id}\n')
                        f.write(f'algorithm: {algo}\n')
                        f.write(f'target_episode: {target_ep}\n')

                    target_ep = int(target_ep)
                    n_ue = int(n_ue) if n_ue is not None else None
                    seed_val = int(seed_val) if seed_val is not None else None
                    batch_sz = int(batch_sz) if batch_sz is not None else None
                    cfg = get_args_with_params(
                        task_size_average=float(task_size_avg) if task_size_avg is not None else None,
                        task_comsumption_average=float(task_cons_avg) if task_cons_avg is not None else None,
                        task_time_average=float(task_time_avg) if task_time_avg is not None else None,
                        task_arrival_rate=float(task_arr_rate) if task_arr_rate is not None else None,
                        n_UE=n_ue,
                        UE_computation_capacity=float(ue_comp_cap) if ue_comp_cap is not None else None,
                        MEC_computation_capacity=float(mec_comp_cap) if mec_comp_cap is not None else None,
                        seed=seed_val
                    )
                    
                    # 写入配置信息
                    with open(log_file, 'a') as f:
                        f.write("\n配置信息:\n")
                        for key, value in cfg.items():
                            f.write(f'{key}: {value}\n')
                    
                    # 简化测试，只验证函数被调用，不执行完整训练
                    env = RuntBoxEnv(cfg)
                    with open(log_file, 'a') as f:
                        f.write("\n环境创建成功\n")
                    model = sb3.SAC('MlpPolicy', env, verbose=1)
                    rewards = []
                    ma_rewards = []
                    for i in range(target_episode):
                        model.learn(total_timesteps=target_episode)
                        ep_reward = test_model(env, model, n_eval_episodes=10, render=True)
                        rewards.append(ep_reward)
                        ma_rewards.append((ma_rewards[-1] * 0.95 + ep_reward * 0.05) if ma_rewards else ep_reward)
                        train_data = TrainData(
                            model_id=model_id,
                            episode=i+1,
                            reward=ep_reward,
                            smoothed_reward=ma_rewards[-1]
                        )
                        train_data.save()
                    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models')
                    file_path = os.path.join(models_dir, f'{rl_model.id}')
                    model.save(file_path)
                    

                    
                except Exception as e:
                    # 记录详细错误信息到文件
                    import traceback
                    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../models/train_error/train_error_{model_id}.txt')
                    with open(log_file, 'w') as f:
                        f.write(f"异步训练失败: {str(e)}\n")
                        f.write(f"错误堆栈: {traceback.format_exc()}\n")
                    # 同时打印到控制台
                    print(f"异步训练失败: {str(e)}")
                    print(f"错误堆栈: {traceback.format_exc()}")

            # 启动异步线程执行训练操作，将所有需要的参数作为函数参数传递
            thread = threading.Thread(
                target=async_train,
                args=(
                    rl_model.id,
                    algorithm,
                    target_episode,
                    task_size_average,
                    task_comsumption_average,
                    task_time_average,
                    task_arrival_rate,
                    n_UE,
                    UE_computation_capacity,
                    MEC_computation_capacity,
                    seed,
                    learning_rate,
                    batch_size,
                    gamma
                )
            )
            thread.daemon = True  # 设置为守护线程，主线程结束时自动退出
            thread.start()
            
            # 返回成功响应
            return JsonResponse({
                'status': 'success', 
                'message': '训练任务创建成功', 
                'id': rl_model.id
            }, status=201)
        
        except Exception as e:
            # 捕获所有异常，返回错误信息
            return JsonResponse({'status': 'error', 'message': f'服务器内部错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)

