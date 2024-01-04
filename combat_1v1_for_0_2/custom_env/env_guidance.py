from custom_env.env_zhikong import Base_env
import param
import random
import gym
import numpy as np
import math


class DogFight(Base_env):
    def __init__(self, config=None, render=0) :
        Base_env.__init__(self, config, render)
        self.collect_num = 0
        self.cur_process_obs = [0 for i in range(self.frame_feature_size)]

    def reset_var(self):
        self.collect_num += 1
        self.cur_process_obs = [0 for i in range(self.frame_feature_size)]

    def set_s_a_space(self):
        """
        define observation space and action space
        """
        self.observation_space = gym.spaces.Box(low=-10, high=10, dtype=np.float64,
                                                shape=(self.frame_feature_size,))
        self.action_space = gym.spaces.Box(low=-1, high=1, dtype=np.float64,
                                                shape=(4,))
        #self.action_space = gym.spaces.Discrete(108)

    def postprocess_action(self, action):
        """
        根据不同的输入形式，选用不同的动作处理方式
        """
        control_side = self.control_side
        action_input = dict()
        obs = self.obs_tot[control_side][f'{control_side}_0']
        elevator_control = action[0] * obs['attitude/pitch-rad'] + action[1] *obs['velocities/q-rad_sec'] # 升降舵控制指令
        rudder_control  = action[2] * obs['attitude/roll-rad'] + action[3]*obs['velocities/p-rad_sec'] # 方向舵控制指令

        action_input[control_side] = {
            f'{control_side}_0': {
                "fcs/rudder-cmd-norm": 1,
                "fcs/elevator-cmd-norm": elevator_control,
            }}
        return action_input

        #return self.input_index_action(action)
    

    def input_index_action(self, action):
        #####################################################################
        # 自身动作的编码
        #####################################################################
        action = int(action)
        switch_missile_action = int(action // 162)
        action %= 162
        launch_missile_action = int(action // 81)
        action %= 81
        action_ce = action // 27 - 1
        action %= 27
        action_ca = action // 9 - 1
        action %= 9
        action_cr = action - 1
        action %= 3
        action_cT = action * 0.5
        #####################################################################
        # 对手策略的生成
        #####################################################################
        control_side = self.control_side
        action_input = dict()
        action_input[control_side] = {
            f'{control_side}_0': {
                "fcs/rudder-cmd-norm": action_cr,
                "fcs/elevator-cmd-norm": action_ce,
                "fcs/throttle-cmd-norm": action_cT,
            }}
        return action_input

    def postprocess_obs(self, obs):
        """
        Args:
            obs: dict format, include all message back from socket,
                 you can normalize obs or postprocess obs here
        Returns:
            postprocessed obs
        """
        obs_control_side = self._common_attribute_state_process()
        obs_control_side = np.array(obs_control_side).clip(-10, 10)
        self.cur_process_obs = obs_control_side
        return obs_control_side

    def get_init_pos(self):
        max_range = 0.3
        red_y = 2 * max_range * np.random.random() - max_range
        blue_y = 2 * max_range * np.random.random() - max_range
        initial_pos_set = [[max_range, -max_range, -90, 90],
                           [-max_range, max_range, 90, -90]]
        initial_pos = random.choice(initial_pos_set)
        r1 = 0.2 * np.random.random() + 0.8
        r2 = 0.2 * np.random.random() + 0.8
        r3 = 0.5 * np.random.random() + 0.5
        r4 = 0.5 * np.random.random() + 0.5
        red_x, blue_x, red_psi, blue_psi = \
            r1 * initial_pos[0], \
            r2 * initial_pos[1], \
            initial_pos[2], \
            initial_pos[3]
        red_v, blue_v = 900 * r3, 900 * r4
        return red_x, red_y, red_psi, red_v, blue_x, blue_y, blue_psi, blue_v

    def get_reward(self, obs):
        """
        Args:
            obs: dict format, include all message back from socket,
                 you can calculate reward according to the obs

        Returns:
            calculated reward
        """
        reward = self.get_win_loss_reward()
        return reward

    def get_win_loss_reward(self):
        """
        Returns:
            win_loss reward
        """
        return 0

    def judge_done(self, obs):
        """
        Args:
            obs: dict format, include all message back from socket,
                 you can judge whether is_done according to the obs

        Returns:
            is_done or not
        """
        max_step_num = param.Max_step_num
        done = {}
        control_side = self.control_side
        life_control_side = self.obs_tot[control_side][f'{control_side}_0']['LifeCurrent']
        IfPresenceHitting_control_side = self.obs_tot[control_side][f'{control_side}_0']['IfPresenceHitting']
        if (not life_control_side and not IfPresenceHitting_control_side) or self.step_num >= max_step_num:
            done['__all__'] = True
        else:
            done['__all__'] = False
        if done['__all__']:
            done['red'] = True
            done['blue'] = True
        else:
            done['red'] = False
            done['blue'] = False
        return done

    def _common_attribute_state_process(self):
        """
        :return: 返回状态编码信息
        """
        control_side = self.control_side
        alley = ['base_state']
        post_process_obs_control_side = []
        post_process_obs_control_side_dict = self._single_player_state_process(flag=control_side)
        for key in alley:
            post_process_obs_control_side.extend(post_process_obs_control_side_dict[key])
        death_control_side = self.death_event()
        #post_process_obs_control_side.extend(death_control_side)
        return post_process_obs_control_side

    def death_event(self):
        control_side = self.control_side
        post_process_obs = []
        control_side_death = self.obs_tot[control_side][f'{control_side}_0']['DeathEvent']
        if control_side_death == 99:
            post_process_obs.append(2)
        elif control_side_death == 0:
            post_process_obs.append(0)
        else:
            post_process_obs.append(1)
        return post_process_obs

    def _single_player_state_process(self, flag):
        """
        :return: 返回编码的状态信息
        """
        post_process_obs = dict()
        post_process_obs['base_state'] = self._state_process(flag=flag)
        return post_process_obs

    def _state_process(self, flag):
        """
        TODO：本函数是状态编码信息，此处只是编码了生命值和高度信息
        TODO：编程开发者可以参考智空文档，自行定义智能体训练需要的观测信息
        """
        if self.is_done[flag]:
            return [0 for i in range(23)]
        else:
            post_process_obs = []
            obs = self.obs_tot[flag][f'{flag}_0']

            # 姿态
            post_process_obs.append(obs['attitude/pitch-rad'])
            post_process_obs.append(obs['attitude/roll-rad'])
            post_process_obs.append(obs['attitude/psi-deg'])

            # 角速度
            post_process_obs.append(obs['velocities/p-rad_sec'])
            post_process_obs.append(obs['velocities/q-rad_sec'])
            post_process_obs.append(obs['velocities/r-rad_sec'])

            return post_process_obs