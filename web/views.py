from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from RUNT_env.RUNT_Environment import RuntBoxEnv
from RUNT_env.config import get_args
from SAC.make_config import get_args_with_params
from .models import User
from .model.rl_model import RLModel
from .model.train_data import TrainData
import os
import decimal
import threading
import stable_baselines3 as sb3
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 模型列表查询接口
@csrf_exempt
def model_list(request):
    """
    查询模型列表，支持分页
    """
    if request.method == 'GET':
        try:
            # 获取分页参数
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)
            
            # 转换为整数
            try:
                page = int(page)
                page_size = int(page_size)
                if page < 1 or page_size < 1:
                    raise ValueError("页码和每页条数必须大于0")
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'参数错误: {str(e)}'}, status=400)
            
            # 获取所有模型数据
            models = RLModel.objects.all().order_by('-create_time')
            
            # 创建分页器
            paginator = Paginator(models, page_size)
            
            try:
                # 获取指定页的数据
                paginated_models = paginator.page(page)
            except PageNotAnInteger:
                # 页码不是整数，返回第一页
                paginated_models = paginator.page(1)
            except EmptyPage:
                # 页码超出范围，返回最后一页
                paginated_models = paginator.page(paginator.num_pages)
            
            # 构造响应数据
            result = {
                'status': 'success',
                'message': '查询成功',
                'data': {
                    'total': paginator.count,
                    'page': paginated_models.number,
                    'page_size': page_size,
                    'total_pages': paginator.num_pages,
                    'models': []
                }
            }
            
            # 转换为字典格式
            for model in paginated_models:
                model_dict = {
                    'id': model.id,
                    'algorithm': model.algorithm,
                    'target_episode': model.target_episode,
                    'current_episode': model.current_episode,
                    'status': model.status,
                    'status_text': dict(model.STATUS_CHOICES).get(model.status, ''),
                    'task_size_average': float(model.task_size_average) if model.task_size_average else None,
                    'task_comsumption_average': float(model.task_comsumption_average) if model.task_comsumption_average else None,
                    'task_time_average': float(model.task_time_average) if model.task_time_average else None,
                    'task_arrival_rate': float(model.task_arrival_rate) if model.task_arrival_rate else None,
                    'n_UE': model.n_UE,
                    'UE_computation_capacity': float(model.UE_computation_capacity) if model.UE_computation_capacity else None,
                    'MEC_computation_capacity': float(model.MEC_computation_capacity) if model.MEC_computation_capacity else None,
                    'seed': model.seed,
                    'learning_rate': float(model.learning_rate) if model.learning_rate else None,
                    'batch_size': model.batch_size,
                    'buffer_size': model.buffer_size,
                    'gamma': float(model.gamma) if model.gamma else None,
                    'create_time': model.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': model.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                result['data']['models'].append(model_dict)
            
            return JsonResponse(result, status=200)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'服务器内部错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

# 模型训练数据查询接口
@csrf_exempt
def model_train_data(request, model_id):
    """
    查询特定模型的训练数据，支持分页
    """
    if request.method == 'GET':
        try:
            # 检查模型是否存在
            try:
                rl_model = RLModel.objects.get(id=model_id)
            except RLModel.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'模型ID {model_id} 不存在'}, status=404)
            
            # 获取分页参数
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 20)
            
            # 转换为整数
            try:
                page = int(page)
                page_size = int(page_size)
                if page < 1 or page_size < 1:
                    raise ValueError("页码和每页条数必须大于0")
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'参数错误: {str(e)}'}, status=400)
            
            # 获取该模型的所有训练数据
            train_datas = TrainData.objects.filter(model_id=model_id).order_by('episode')
            
            # 创建分页器
            paginator = Paginator(train_datas, page_size)
            
            try:
                # 获取指定页的数据
                paginated_train_datas = paginator.page(page)
            except PageNotAnInteger:
                # 页码不是整数，返回第一页
                paginated_train_datas = paginator.page(1)
            except EmptyPage:
                # 页码超出范围，返回最后一页
                paginated_train_datas = paginator.page(paginator.num_pages)
            
            # 构造响应数据
            result = {
                'status': 'success',
                'message': '查询成功',
                'data': {
                    'model_id': model_id,
                    'model_algorithm': rl_model.algorithm,
                    'total': paginator.count,
                    'page': paginated_train_datas.number,
                    'page_size': page_size,
                    'total_pages': paginator.num_pages,
                    'train_data': []
                }
            }
            
            # 转换为字典格式
            for train_data in paginated_train_datas:
                train_data_dict = {
                    'id': train_data.id,
                    'episode': train_data.episode,
                    'reward': float(train_data.reward) if train_data.reward else None,
                    'smoothed_reward': float(train_data.smoothed_reward) if train_data.smoothed_reward else None,
                    'create_time': train_data.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': train_data.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                result['data']['train_data'].append(train_data_dict)
            
            return JsonResponse(result, status=200)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'服务器内部错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

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
                    # 确保日志目录存在
                    os.makedirs(os.path.dirname(log_file), exist_ok=True)
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
                    
                    # 创建环境
                    env = RuntBoxEnv(cfg)
                    with open(log_file, 'a') as f:
                        f.write("\n环境创建成功\n")

                    learning_rate = float(lr) if lr is not None else 3e-4
                    batch_size = batch_sz if batch_sz is not None else 256
                    gamma = float(gamma_val) if gamma_val is not None else 0.99
                    
                    # 创建模型，配置超参数
                    model = sb3.SAC(
                        'MlpPolicy', 
                        env, 
                        verbose=1,
                        learning_rate=learning_rate,
                        batch_size=batch_size,
                        gamma=gamma,
                        tau=0.005,
                        buffer_size=1000000,
                        learning_starts=1000,
                        policy_kwargs=dict(net_arch=[256, 256])
                    )
                    
                    # 写入模型配置信息
                    with open(log_file, 'a') as f:
                        f.write("\n模型配置:\n")
                        f.write(f'learning_rate: {learning_rate}\n')
                        f.write(f'batch_size: {batch_size}\n')
                        f.write(f'gamma: {gamma}\n')
                    
                    rewards = []
                    ma_rewards = []
                    episode_timesteps = 1000
                    for i in range(target_ep):
                        # 写入回合开始信息
                        with open(log_file, 'a') as f:
                            f.write(f"\n第{i+1}回合开始训练\n")
                        
                        # 训练固定步数，并将返回的更新后模型赋值给model变量
                        model = model.learn(total_timesteps=episode_timesteps)
                        
                        # 测试模型
                        ep_reward = test_model(env, model, n_eval_episodes=10, render=True)
                        
                        # 记录奖励
                        rewards.append(ep_reward)
                        ma_rewards.append((ma_rewards[-1] * 0.95 + ep_reward * 0.05) if ma_rewards else ep_reward)
                        
                        # 写入奖励信息
                        with open(log_file, 'a') as f:
                            f.write(f"第{i+1}回合奖励: {ep_reward:.4f}, 平滑奖励: {ma_rewards[-1]:.4f}\n")
                        
                        # 保存到数据库
                        train_data = TrainData(
                            model_id=model_id,
                            episode=i+1,
                            reward=ep_reward,
                            smoothed_reward=ma_rewards[-1]
                        )
                        train_data.save()
                    
                    # 保存模型
                    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models')
                    file_path = os.path.join(models_dir, f'{model_id}')
                    model.save(file_path)
                    
                    # 写入训练完成信息
                    with open(log_file, 'a') as f:
                        f.write("\n训练完成！\n")

                except Exception as e:
                    # 记录详细错误信息到文件
                    import traceback
                    error_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models/train_error')
                    os.makedirs(error_dir, exist_ok=True)
                    log_file = os.path.join(error_dir, f'train_error_{model_id}.txt')
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

@csrf_exempt
def testmodel(request):
    """
    模型推理接口
    接收model_id和初始observation，执行100步推理并返回结果
    """
    if request.method == 'POST':
        try:
            import json
            import numpy as np
            # 解析JSON请求体
            request_data = json.loads(request.body)
            
            # 1. 输入验证
            # 验证model_id
            model_id = request_data.get('model_id')
            if not model_id or not isinstance(model_id, str) or model_id.strip() == '':
                return JsonResponse({'status': 'error', 'message': 'model_id必须是非空字符串'}, status=400)
            
            # 验证observation
            observation = request_data.get('observation')
            if not observation or not isinstance(observation, list):
                return JsonResponse({'status': 'error', 'message': 'observation必须是浮点数数组'}, status=400)
            
            # 验证observation中的元素是否为浮点数
            try:
                observation = [float(x) for x in observation]
            except (ValueError, TypeError):
                return JsonResponse({'status': 'error', 'message': 'observation数组中的元素必须是有效的浮点数'}, status=400)
            
            # 2. 模型和环境初始化
            # 查询模型信息
            try:
                rl_model = RLModel.objects.get(id=model_id)
            except RLModel.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'模型ID {model_id} 不存在'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'数据库查询错误: {str(e)}'}, status=500)
            
            # 获取n_ues值
            n_ues = rl_model.n_UE
            if not n_ues:
                return JsonResponse({'status': 'error', 'message': '模型缺少n_UE参数'}, status=500)
            
            # 计算expected observation size
            expected_obs_size = 4 * n_ues + 4
            if len(observation) != expected_obs_size:
                return JsonResponse({'status': 'error', 'message': f'observation数组大小不匹配，预期大小为{expected_obs_size}，实际大小为{len(observation)}'}, status=400)
            
            # 构造配置
            cfg = get_args_with_params(
                task_size_average=float(rl_model.task_size_average) if rl_model.task_size_average else None,
                task_comsumption_average=float(rl_model.task_comsumption_average) if rl_model.task_comsumption_average else None,
                task_time_average=float(rl_model.task_time_average) if rl_model.task_time_average else None,
                task_arrival_rate=float(rl_model.task_arrival_rate) if rl_model.task_arrival_rate else None,
                n_UE=n_ues,
                UE_computation_capacity=float(rl_model.UE_computation_capacity) if rl_model.UE_computation_capacity else None,
                MEC_computation_capacity=float(rl_model.MEC_computation_capacity) if rl_model.MEC_computation_capacity else None,
                seed=rl_model.seed
            )
            
            # 初始化环境
            try:
                env = RuntBoxEnv(cfg)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'环境初始化失败: {str(e)}'}, status=500)
            
            # 加载预训练模型
            try:
                model = sb3.SAC("MlpPolicy", env, verbose=1, learning_rate=0.00003, tensorboard_log='./SAC/')
                model.load('models/'+model_id+'.zip')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'模型加载失败: {str(e)}'}, status=500)
            
            # 3. 推理执行
            # 初始化存储结果的数组
            observations = []
            actions = []
            rewards = []
            
            # 执行100步推理
            obs = np.array(observation, dtype=np.float32)
            for step in range(100):
                # 生成动作
                action, _ = model.predict(obs, deterministic=True)
                
                # 执行环境步骤
                next_obs, reward, done, _ = env.step(action)
                
                # 转换为适当的float类型
                action = [float(x) for x in action]
                obs_float = [float(x) for x in obs]
                reward_float = float(reward)
                
                # 存储结果
                observations.append(obs_float)
                actions.append(action)
                rewards.append(reward_float)
                
                # 更新obs为下一个观测值
                obs = next_obs
            
            # 4. 响应构造
            response_data = {
                'observation': observations,
                'action': actions,
                'rewards': rewards
            }
            
            return JsonResponse(response_data, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON格式'}, status=400)
        except Exception as e:
            # 捕获所有其他异常
            return JsonResponse({'status': 'error', 'message': f'服务器内部错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)