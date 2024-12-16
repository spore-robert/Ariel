from stable_baselines3 import PPO
#from SoldierEnv_Mlp import SoldierEnv_Mlp
from SoldierEnv2 import SoldierEnv
# 創建環境
env = SoldierEnv()

# 初始化 PPO 模型
model = PPO("MlpPolicy", env, verbose=1)

# 訓練模型
model.learn(total_timesteps=100000)

# 保存模型
model.save("../Shooter/model_data/model_mlpPolicy")
#model.save("model_mlpPolicy")
