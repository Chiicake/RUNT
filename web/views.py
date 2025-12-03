from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import User
from .model.rl_model import RLModel
import os
import decimal

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
            current_episode = request.POST.get('current_episode', '0')
            status = request.POST.get('status', '0')
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
            
            try:
                current_episode = int(current_episode)
                if current_episode < 0:
                    return JsonResponse({'status': 'error', 'message': 'current_episode必须为非负整数'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'current_episode必须为整数'}, status=400)
            
            try:
                status = int(status)
                if status not in [0, 1]:
                    return JsonResponse({'status': 'error', 'message': 'status必须为0或1'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'status必须为整数'}, status=400)
            
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
                    current_episode=current_episode,
                    status=status,
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
                
                # 创建以id命名的txt文件
                models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
                file_path = os.path.join(models_dir, f'{rl_model.id}.txt')
                
                try:
                    with open(file_path, 'w') as f:
                        f.write(f'RL Model ID: {rl_model.id}\n')
                        f.write(f'Algorithm: {rl_model.algorithm}\n')
                        f.write(f'Target Episode: {rl_model.target_episode}\n')
                        f.write(f'Current Episode: {rl_model.current_episode}\n')
                        f.write(f'Status: {rl_model.status}\n')
                        f.write(f'Create Time: {rl_model.create_time}\n')
                except Exception as e:
                    # 文件创建失败，事务会自动回滚
                    return JsonResponse({'status': 'error', 'message': f'文件创建失败: {str(e)}'}, status=500)
            
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

