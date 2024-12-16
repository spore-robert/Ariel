import gym
from gym import spaces
import numpy as np

class SoldierEnv(gym.Env):
    def __init__(self):
        super(SoldierEnv, self).__init__()
        
        # 動作空間：4 種動作
        self.action_space = spaces.Discrete(4)
        
        # 狀態空間：AI 和 Player 的相對位置 + 血量 + 彈藥
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
        
        # 初始化遊戲狀態
        self.reset()

    def reset(self):
        # 重置遊戲狀態
        self.ai_x = 0.5
        self.ai_y = 0.5
        self.player_x = 0.8
        self.player_y = 0.5
        self.health = 1.0
        self.ammo = 1.0
        
        return self.get_state()

    def step(self, action):
        reward = 0
        done = False
        
        # 根據動作更新遊戲狀態
        if action == 0:  # Move left
            self.ai_x = max(0, self.ai_x - 0.05)
        elif action == 1:  # Move right
            self.ai_x = min(1, self.ai_x + 0.05)
        elif action == 2:  # Jump
            reward += 0.1  # 獎勵跳躍行為
        elif action == 3:  # Shoot
            if self.ammo > 0:
                self.ammo -= 0.1
                reward += 0.5  # 獎勵射擊行為
            
        # 計算與玩家的距離
        distance_to_player = abs(self.ai_x - self.player_x) + abs(self.ai_y - self.player_y)
        
        # 獎勵靠近玩家的行為
        reward += 1 - distance_to_player
        
        # 更新健康值（簡單模擬被攻擊）
        self.health -= 0.01
        
        # 判定遊戲是否結束
        if self.health <= 0:
            done = True
            reward -= 1  # 遊戲結束懲罰
            
        return self.get_state(), reward, done, {}

    def get_state(self):
        # 返回正規化的狀態
        return np.array([
            self.ai_x,
            self.ai_y,
            self.player_x,
            self.player_y,
            self.health,
            self.ammo
        ], dtype=np.float32)
