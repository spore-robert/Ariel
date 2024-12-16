import gym
from gym import spaces
import numpy as np
import random
import pygame

# 定義環境
class SoldierEnv(gym.Env):
    def __init__(self):
        super(SoldierEnv, self).__init__()

        # 動作空間：4 種動作 (左移, 右移, 跳躍, 開火)
        self.action_space = spaces.Discrete(4)
        
        # 狀態空間：AI 和 Player 的相對位置 + 血量 + 彈藥
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
        
        # 初始化遊戲狀態
        self.reset()

    def reset(self):
        # 重置遊戲狀態
        self.ai_x = 1.0  # AI 初始位置在玩家右側
        self.ai_y = 0.5  # AI 垂直位置
        self.player_x = 0.0  # 玩家從左邊開始
        self.player_y = 0.5  # 玩家垂直位置
        self.health = 1.0  # AI 初始血量
        self.ammo = 1.0  # 初始彈藥
        self.ai_appear_threshold = 0.5  # 玩家達到此位置後，敵人開始射擊
        self.vision_range = 0.5  # 敵人的視野範圍
        
        return self.get_state()

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

    def step(self, action):
        reward = 0
        done = False
    
        # 根據動作更新遊戲狀態
        if action == 0:  # Move left
            self.ai_x = max(0, self.ai_x - 0.05)
        elif action == 1:  # Move right
            self.ai_x = min(1, self.ai_x + 0.05)
        elif action == 2:  # Jump
            reward += 0.1  # 獎勳跳躍行為
        elif action == 3:  # Shoot
            if self.ammo > 0:
                self.ammo -= 0.1
                reward += 0.5  # 獎勳射擊行為
    
        # 玩家持續向右移動
        self.player_x = min(1, self.player_x + 0.01)  # 玩家每步向右移動
    
        # 計算與玩家的距離
        distance_to_player = abs(self.ai_x - self.player_x)
    
        # 檢查是否需要讓敵人出現
        if self.player_x >= self.ai_appear_threshold:
            self.ai_x = 0.8  # 讓敵人出現在玩家面前
            reward += 0.2  # 玩家靠近敵人獲得獎勳
    
        # 讓敵人狙擊玩家：當玩家在射程內，敵人會立刻射擊
        if distance_to_player < 0.3:  # 設定射擊範圍
            reward += 1.0  # 獎勳敵人狙擊行為
            # 假設玩家被擊中，遊戲結束
            self.health = 0  # 玩家被擊中
            done = True  # 遊戲結束
    
        # 更新健康值（簡單模擬被攻擊）
        self.health -= 0.01
        
        # 判定遊戲是否結束
        if self.health <= 0:
            done = True
            reward -= 1  # 遊戲結束懲罰
    
        # 返回新的狀態、獎勳、遊戲是否結束和額外信息
        return self.get_state(), reward, done, {}



     
