import math

obs_control_info = {
    'position/h-sl-ft': 100000,   # 海拔高度 [ft]
    'attitude/pitch-rad': 1,     # 俯仰角[rad]
    'attitude/roll-rad': 1,    # 翻滚角 [rad]
    'attitude/psi-deg': 57.3,       # 航向角 [度]
    'aero/beta-deg': 57.3,        # 侧滑角 [度]
    'aero/alpha-deg': 57.3,       # 攻角 [度]
    'position/lat-geod-deg': 1,   # 纬度 [度]
    'position/long-gc-deg': 1,   # 纬度 [度]
    'velocities/u-fps': 1000,     # 机体坐标系 x 轴速度 [ft/s]
    'velocities/v-fps': 1000,    # 机体坐标系 y 轴速度 [ft/s]
    'velocities/w-fps': 1000,     # 机体坐标系 z 轴速度 [ft/s]
    'velocities/v-north-fps': 1000,    # 北方向速度 [ft/s]
    'velocities/v-east-fps': 1000,    # 东方向速度 [ft/s]
    'velocities/v-down-fps': 1000,   # 向下方向速度 [ft/s]
    'accelerations/a-pilot-x-ft_sec2': 100,    # 飞机坐标系 x轴加速度[ft/s2]
    'accelerations/a-pilot-y-ft_sec2': 100,  # 飞机坐标系 y轴加速度[ft/s2]
    'accelerations/a-pilot-z-ft_sec2': 100,   # 飞机坐标系 z轴加速度[ft/s2]
    'accelerations/n-pilot-x-norm': 10,    # 飞机坐标系x轴加速度
    'accelerations/n-pilot-y-norm': 10,    # 飞机坐标系y轴加速度
    'accelerations/n-pilot-z-norm': 10,      # 飞机坐标系z轴加速度
    'velocities/p-rad_sec': 1,     # 翻滚速率 [rad/s]
    'velocities/q-rad_sec': 1,    # 翻滚速率 [rad/s]
    'velocities/r-rad_sec': 1,   # 偏航速率 [rad/s]
    'velocities/ve-fps': 1000,          # 真实速度 [ft/s]
    'velocities/h-dot-fps': 1000,     # 高度变化速率 [ft/s]
    'velocities/mach': 1,         # 马赫[M]
    'forces/load-factor': 10,   # 负载系数
    'fcs/left-aileron-pos-norm': 1,     # 左副翼位置(-1,1)
    'fcs/right-aileron-pos-norm': 1,      # 右副翼位置(-1,1)
    'fcs/elevator-pos-norm': 1,        # 升降舵位置(-1,1)
    'fcs/rudder-pos-norm': 1,       # 方向舵位置(-1,1)
    'fcs/throttle-pos-norm': 1,       # 油门位置(0,1)
    'gear/gear-pos-norm': 1,      # 起落架位置(0,1)
    'propulsion/engine/set-running': 1,       # 发动机运转
    'propulsion/set-running': 1,      # 设置引擎运行
    'propulsion/engine/thrust-lbs': 1000,       # 发动机推力 [lb]
    'propulsion/tank/pct-full': 100,       # 获取油箱的加注液位，
    'fcs/aileron-cmd-norm': 1,        # 副翼指令(-1,1)
    'fcs/elevator-cmd-norm': 1,      # 升降舵指令 (-1,1)
    'fcs/rudder-cmd-norm': 1,        # 方向舵指令(-1,1)
    'fcs/throttle-cmd-norm': 1,       # 油门指令(0,1)
    'fcs/mixture-cmd-norm': 1,        # 发动机混合设置(0,1)
    'fcs/throttle-cmd-norm[1]': 1,        # 油门 1 指令位置(0,1)
    'fcs/mixture-cmd-norm[1]': 1,     # 油料混合调整阀1 设置(0,1)
    }


obs_info = {
    'position/h-sl-ft': 100000,   # 海拔高度 [ft]
    'attitude/pitch-rad': 1,     # 俯仰角[rad]
    'attitude/roll-rad': 1,    # 翻滚角 [rad]
    'attitude/psi-deg': 57.3,       # 航向角 [度]
    'aero/beta-deg': 57.3,        # 侧滑角 [度]
    'aero/alpha-deg': 57.3,       # 攻角 [度]
    'position/lat-geod-deg': 1,   # 纬度 [度]
    'position/long-gc-deg': 1,   # 纬度 [度]
    'velocities/u-fps': 1000,     # 机体坐标系 x 轴速度 [ft/s]
    'velocities/v-fps': 1000,    # 机体坐标系 y 轴速度 [ft/s]
    'velocities/w-fps': 1000,     # 机体坐标系 z 轴速度 [ft/s]
    'velocities/v-north-fps': 1000,    # 北方向速度 [ft/s]
    'velocities/v-east-fps': 1000,    # 东方向速度 [ft/s]
    'velocities/v-down-fps': 1000,   # 向下方向速度 [ft/s]
    'accelerations/a-pilot-x-ft_sec2': 100,    # 飞机坐标系 x轴加速度[ft/s2]
    'accelerations/a-pilot-y-ft_sec2': 100,  # 飞机坐标系 y轴加速度[ft/s2]
    'accelerations/a-pilot-z-ft_sec2': 100,   # 飞机坐标系 z轴加速度[ft/s2]
    'accelerations/n-pilot-x-norm': 10,    # 飞机坐标系x轴加速度
    'accelerations/n-pilot-y-norm': 10,    # 飞机坐标系y轴加速度
    'accelerations/n-pilot-z-norm': 10,      # 飞机坐标系z轴加速度
    'velocities/p-rad_sec': 1,     # 翻滚速率 [rad/s]
    'velocities/q-rad_sec': 1,    # 翻滚速率 [rad/s]
    'velocities/r-rad_sec': 1,   # 偏航速率 [rad/s]
    'velocities/ve-fps': 1000,          # 真实速度 [ft/s]
    'velocities/h-dot-fps': 1000,     # 高度变化速率 [ft/s]
    'velocities/mach': 1,         # 马赫[M]
    'forces/load-factor': 10,   # 负载系数
    'fcs/left-aileron-pos-norm': 1,     # 左副翼位置(-1,1)
    'fcs/right-aileron-pos-norm': 1,      # 右副翼位置(-1,1)
    'fcs/elevator-pos-norm': 1,        # 升降舵位置(-1,1)
    'fcs/rudder-pos-norm': 1,       # 方向舵位置(-1,1)
    'fcs/throttle-pos-norm': 1,       # 油门位置(0,1)
    'gear/gear-pos-norm': 1,      # 起落架位置(0,1)
    'propulsion/engine/set-running': 1,       # 发动机运转
    'propulsion/set-running': 1,      # 设置引擎运行
    'propulsion/engine/thrust-lbs': 1000,       # 发动机推力 [lb]
    'propulsion/tank/pct-full': 100,       # 获取油箱的加注液位，
    'fcs/aileron-cmd-norm': 1,        # 副翼指令(-1,1)
    'fcs/elevator-cmd-norm': 1,      # 升降舵指令 (-1,1)
    'fcs/rudder-cmd-norm': 1,        # 方向舵指令(-1,1)
    'fcs/throttle-cmd-norm': 1,       # 油门指令(0,1)
    'fcs/mixture-cmd-norm': 1,        # 发动机混合设置(0,1)
    'fcs/throttle-cmd-norm[1]': 1,        # 油门 1 指令位置(0,1)
    'fcs/mixture-cmd-norm[1]': 1,     # 油料混合调整阀1 设置(0,1)
    # 态势信息
    'target_longdeg': 1,            # 目标经度[度]
    'target_latdeg': 1,             # 目标纬度[度]
    'target_altitude_ft': 100000,   # 目标高度[ft]
    'target_velocity': 1000,        # 目标速度[ft/s]
    'target_track_deg': 57.3,       # 目标航向[度]
    'altitude_error_ft': 100000,    # 高度误差（当前-目标））
    'track_error_deg': 57.3,        # 航向误差（当前-目标
    'delta_velocity': 1000,         # 速度误差（目标-当前）
    'missile-launch': 1,            # 发射导弹
    'bullet-launch': 1,             # 发射子弹
    'LifeCurrent': 200,             # 生命值（初始值200）
    'BulletCurrentNum': 510,        # 剩余子弹数（初始100发）
    'SRAAMCurrentNum': 4,           # 近程红外弹数量（初始4枚）
    'SRAAM1_CanReload': 1,          # 近程红外弹1发射口是否已经装配好[0/1]
    'SRAAM2_CanReload': 1,          # 近程红外弹1发射口是否已经装配好[0/1]
    'SRAAMTargetLocked': 9,         # 目标状态下锁定敌方编号（单个数字表示） 9 表示未锁定目标
    'AMRAAMCurrentNum': 8,          # 中程雷达弹剩余数量（初始8枚）
    'AMRAAM1_CanReload': 1,         # 中程雷达弹1发射口是否已经装配好[0/1]
    'AMRAAM2_CanReload': 1,         # 中程雷达弹2发射口是否已经装配好[0/1]
    'AMRAAM3_CanReload': 1,         # 中程雷达弹3发射口是否已经装配好[0/1]
    'AMRAAM4_CanReload': 1,         # 中程雷达弹4发射口是否已经装配好[0/1]
    'MissileAlert': 1,              # 是否被雷达弹锁定1/0
    'WarningNumber': 3,             # 战机所发射的导弹可否击中目标1/0
    'IsOutOfValidBattleArea': 1,    # 战机是否在战区外 1/0
    'IfPresenceHitting': 1,         # 战机所发射的导弹可否击中目标1/0
    }
