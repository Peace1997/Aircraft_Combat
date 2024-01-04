import param
from custom_env.dog_flight import DogFight
import os
import atexit
import torch
from utils.obs_config import *
import copy
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym


def exit():
    os.system("ps -ef|grep ZK.x86_64|grep -v grep |awk '{print $2}'|xargs kill -9")
    os.system("taskkill /F /IM ZK.exe")

if __name__ == "__main__":
    args = param.parser.parse_args()
    args.excute_path = r'D:\combat_env\Windows\ZK.exe'
    args.save_folder = 'data/output/tmp'
    args.checkpoint = None
    args.render = 1
    args.lr = 1e-5
    args.red_num = 1
    args.blue_num = 1
    obs_c_i = obs_control_info.copy()
    obs_a_i = obs_info.copy()
    args.frame_feature_size = 3
    args.obs_c_i = obs_c_i
    args.obs_c_FFS = len(obs_c_i)
    args.a_c_FFS = 4
    args.obs_a_i = obs_a_i
    args.obs_w_FFS = len(obs_a_i) + 8

    config = {
        "env": DogFight,
        "env_config": {
            "render": args.render,
            'ip': '127.0.1.1',
            'port': args.port + 100,
            'Red': 0,
            'Blue': 2,  # Red和Blue用于通信，不同通信方式见文档
            'mode': 'train',
            'usage': 'train',
            "excute_path": args.excute_path,
            "frame_feature_size": args.frame_feature_size,
            'control_side': 'red',
        },
        'recreate_failed_workers': True,
        "num_gpus": args.num_gpus,
        "lr": args.lr,
        "num_workers": args.num_workers,
        "use_gae": True,
        "lambda": 0.99,
        'model': {'fcnet_activation': 'tanh',
                  'custom_model_config': {}},

        'evaluation_num_workers': args.evaluation_num_workers,
        'evaluation_interval': args.evaluation_interval,
        'evaluation_config': {
            'exploration': False,
            "env_config": {
                "render": args.render,
                'ip': '127.0.1.1',
                'port': args.port,
                'mode': 'eval',
                'usage': 'train',
                "excute_path": args.excute_path,
                "frame_feature_size": args.frame_feature_size,
                'control_side': 'red',
            },
        },
        'evaluation_duration': args.evaluation_duration,
        "evaluation_duration_unit": "episodes",

        'seed': args.randomseed,
        "batch_mode": "complete_episodes",
        "train_batch_size": 500,  # 每次训练的数据批，数据批越大，差距越小
        'sgd_minibatch_size': 250,  # 每次mini-batch-size的大小，这个值越大，计算越省时，主要也得看gpu是否使用，如果gpu不用，那大了也没意义
        "framework": "torch",
    }