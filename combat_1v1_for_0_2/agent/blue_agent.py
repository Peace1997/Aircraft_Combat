from agent.base_agent import Base_agent
import param
import random
import gym
import numpy as np
import math


class Blue_agent(Base_agent):
    def __init__(self, control_num, side, agent_config):
        super().__init__(control_num, side, agent_config)

    def agent_step(self, obs):
        """
        TODO: 在此处可以定义对手的动作，下面的例子是给予了一个平飞的操作，对手采用平飞策略，但是不发射武器
        """
        obs = obs[f'blue_0']
        control_side_psi, control_side_v, control_side_h = \
            obs['attitude/psi-deg'], \
            math.sqrt(obs['velocities/u-fps'] ** 2 +
                      obs['velocities/v-fps'] ** 2 +
                      obs['velocities/w-fps'] ** 2), \
            obs['position/h-sl-ft']
        opponent_action = {
            f'blue_0': {
                'mode': 2,
                "target_altitude_ft": control_side_h,
                "target_velocity": control_side_v,
                "target_track_deg": control_side_psi,
                "fcs/weapon-launch": 0,
                "switch-missile": 0,
                "change-target": 9,
            }}
        return opponent_action

