from django.test import TestCase, Client
from django.urls import reverse
from .model.rl_model import RLModel
from .model.train_data import TrainData
import json


class ModelAPITestCase(TestCase):
    """
    测试模型相关API接口
    """
    
    def setUp(self):
        """
        测试前的准备工作，创建测试数据
        """
        self.client = Client()
        
        # 创建测试模型
        self.model1 = RLModel.objects.create(
            algorithm="DQN",
            target_episode=100,
            current_episode=0,
            status=0,
            task_size_average=1024.5,
            task_comsumption_average=512.25,
            task_time_average=10.5,
            task_arrival_rate=2.5,
            n_UE=10,
            UE_computation_capacity=10000.0,
            MEC_computation_capacity=100000.0,
            seed=42,
            learning_rate=0.0001,
            batch_size=64,
            gamma=0.99
        )
        
        self.model2 = RLModel.objects.create(
            algorithm="SAC",
            target_episode=200,
            current_episode=50,
            status=0,
            task_size_average=2048.0,
            task_comsumption_average=1024.0,
            task_time_average=20.0,
            task_arrival_rate=5.0,
            n_UE=20,
            UE_computation_capacity=20000.0,
            MEC_computation_capacity=200000.0,
            seed=123,
            learning_rate=0.0003,
            batch_size=128,
            gamma=0.98
        )
        
        # 为model1创建训练数据
        for i in range(1, 6):
            TrainData.objects.create(
                model=self.model1,
                episode=i,
                reward=-2000.0 + i * 100,
                smoothed_reward=-2000.0 + i * 100
            )
        
        # 为model2创建训练数据
        for i in range(1, 11):
            TrainData.objects.create(
                model=self.model2,
                episode=i,
                reward=-3000.0 + i * 150,
                smoothed_reward=-3000.0 + i * 150
            )
    
    def test_model_list_get(self):
        """
        测试模型列表查询接口
        """
        url = reverse('model_list')
        
        # 测试默认分页参数
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['total'], 2)
        self.assertEqual(data['data']['page'], 1)
        self.assertEqual(data['data']['page_size'], 10)
        self.assertEqual(data['data']['total_pages'], 1)
        self.assertEqual(len(data['data']['models']), 2)
        
        # 测试自定义分页参数
        response = self.client.get(url, {'page': 1, 'page_size': 1})
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['total'], 2)
        self.assertEqual(data['data']['page'], 1)
        self.assertEqual(data['data']['page_size'], 1)
        self.assertEqual(data['data']['total_pages'], 2)
        self.assertEqual(len(data['data']['models']), 1)
        
        # 测试第二页
        response = self.client.get(url, {'page': 2, 'page_size': 1})
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['page'], 2)
        self.assertEqual(len(data['data']['models']), 1)
        
        # 测试无效页码
        response = self.client.get(url, {'page': -1, 'page_size': 10})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        
        response = self.client.get(url, {'page': 1, 'page_size': 0})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
    
    def test_model_train_data_get(self):
        """
        测试模型训练数据查询接口
        """
        # 测试model1的训练数据
        url = reverse('model_train_data', kwargs={'model_id': self.model1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['model_id'], self.model1.id)
        self.assertEqual(data['data']['model_algorithm'], self.model1.algorithm)
        self.assertEqual(data['data']['total'], 5)
        self.assertEqual(data['data']['page'], 1)
        self.assertEqual(data['data']['page_size'], 20)
        self.assertEqual(data['data']['total_pages'], 1)
        self.assertEqual(len(data['data']['train_data']), 5)
        
        # 测试model2的训练数据，使用自定义分页参数
        url = reverse('model_train_data', kwargs={'model_id': self.model2.id})
        response = self.client.get(url, {'page': 1, 'page_size': 5})
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['model_id'], self.model2.id)
        self.assertEqual(data['data']['total'], 10)
        self.assertEqual(data['data']['page'], 1)
        self.assertEqual(data['data']['page_size'], 5)
        self.assertEqual(data['data']['total_pages'], 2)
        self.assertEqual(len(data['data']['train_data']), 5)
        
        # 测试第二页
        response = self.client.get(url, {'page': 2, 'page_size': 5})
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['page'], 2)
        self.assertEqual(len(data['data']['train_data']), 5)
        
        # 测试无效模型ID
        url = reverse('model_train_data', kwargs={'model_id': 999})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'error')
        
        # 测试无效页码
        url = reverse('model_train_data', kwargs={'model_id': self.model1.id})
        response = self.client.get(url, {'page': -1, 'page_size': 10})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
    
    def test_model_list_post_method_not_allowed(self):
        """
        测试模型列表接口不允许POST方法
        """
        url = reverse('model_list')
        response = self.client.post(url, {})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['status'], 'error')
    
    def test_model_train_data_post_method_not_allowed(self):
        """
        测试模型训练数据接口不允许POST方法
        """
        url = reverse('model_train_data', kwargs={'model_id': self.model1.id})
        response = self.client.post(url, {})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['status'], 'error')
