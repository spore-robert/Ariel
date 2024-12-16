from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from SoldierEnv_dqn import SoldierEnv
# 初始化環境
env = SoldierEnv()

# 設定 DQN 超參數
model = DQN(
    "MlpPolicy",              # 使用多層感知器的策略網路
    env,                      # 使用自定義的環境
    learning_rate=0.001,      # 學習率
    buffer_size=10000,        # 重播緩衝區大小
    learning_starts=1000,     # 開始學習前收集的經驗步數
    batch_size=32,            # 批次大小
    tau=1.0,                  # 軟更新的參數
    gamma=0.99,               # 折扣因子
    train_freq=4,             # 每 4 步訓練一次
    target_update_interval=500, # 更新目標網路的間隔
    verbose=1,                # 訓練過程的輸出級別
)

# 開始訓練模型
model.learn(total_timesteps=100000)

# 保存模型
model.save("../Shooter/model_data/model_dqn")
#model.save("model_dqn")

# 測試模型
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"平均獎勵: {mean_reward} +/- {std_reward}")
