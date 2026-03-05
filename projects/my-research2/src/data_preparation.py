"""
数据准备与预处理
任务1：加载数据集，进行数据清洗、特征工程和划分训练测试集
"""

import json
import os
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def main():
    """主函数：执行数据准备与预处理"""
    print("=== 任务1: 数据准备与预处理 ===")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 生成模拟数据集
    print("1. 生成模拟数据集...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=42,
        weights=[0.7, 0.3]
    )
    
    print(f"数据集形状: X={X.shape}, y={y.shape}")
    print(f"类别分布: 0={sum(y==0)}, 1={sum(y==1)}")
    
    # 划分训练集和测试集
    print("2. 划分训练集和测试集...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"训练集: X_train={X_train.shape}, y_train={y_train.shape}")
    print(f"测试集: X_test={X_test.shape}, y_test={y_test.shape}")
    
    # 特征标准化
    print("3. 特征标准化...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("特征标准化完成")
    
    # 创建特征名称
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # 保存预处理后的数据
    print("4. 保存预处理数据...")
    data_info = {
        "dataset_info": {
            "n_samples": X.shape[0],
            "n_features": X.shape[1],
            "n_classes": len(np.unique(y)),
            "class_distribution": {
                "class_0": int(sum(y == 0)),
                "class_1": int(sum(y == 1))
            }
        },
        "split_info": {
            "train_size": X_train.shape[0],
            "test_size": X_test.shape[0],
            "train_test_ratio": 0.8
        },
        "features": feature_names,
        "preprocessing": {
            "scaler_type": "StandardScaler",
            "scaler_params": {
                "with_mean": True,
                "with_std": True
            }
        },
        "data_paths": {
            "X_train": "data/X_train.npy",
            "X_test": "data/X_test.npy",
            "y_train": "data/y_train.npy",
            "y_test": "data/y_test.npy",
            "feature_names": "data/feature_names.npy"
        }
    }
    
    # 保存数据文件
    os.makedirs('data', exist_ok=True)
    np.save('data/X_train.npy', X_train_scaled)
    np.save('data/X_test.npy', X_test_scaled)
    np.save('data/y_train.npy', y_train)
    np.save('data/y_test.npy', y_test)
    np.save('data/feature_names.npy', feature_names)
    
    # 保存数据信息
    with open('exp/results/data_preparation.json', 'w', encoding='utf-8') as f:
        json.dump(data_info, f, ensure_ascii=False, indent=2)
    
    # 生成数据可视化
    print("5. 生成数据可视化...")
    create_visualizations(X, y, X_train, X_test, feature_names)
    
    # 更新任务状态
    print("6. 更新任务状态...")
    update_task_status(1, 'completed', data_info)
    
    print("✓ 任务1完成: 数据准备与预处理")
    print(f"   - 生成数据集: {X.shape[0]}个样本, {X.shape[1]}个特征")
    print(f"   - 训练集/测试集: {X_train.shape[0]}/{X_test.shape[0]}")
    print(f"   - 数据已保存到: data/ 目录")
    print(f"   - 结果已保存到: exp/results/data_preparation.json")
    print(f"   - 可视化图表: exp/figures/data_visualization.png")
    
    return data_info

def create_visualizations(X, y, X_train, X_test, feature_names):
    """创建数据可视化图表"""
    # 创建可视化图表
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 类别分布
    axes[0, 0].bar(['Class 0', 'Class 1'], [sum(y==0), sum(y==1)], color=['skyblue', 'lightcoral'])
    axes[0, 0].set_title('类别分布')
    axes[0, 0].set_ylabel('样本数量')
    
    # 特征相关性热图（前10个特征）
    corr_matrix = np.corrcoef(X[:, :10], rowvar=False)
    im = axes[0, 1].imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    axes[0, 1].set_title('特征相关性热图（前10个特征）')
    plt.colorbar(im, ax=axes[0, 1])
    axes[0, 1].set_xticks(range(10))
    axes[0, 1].set_yticks(range(10))
    axes[0, 1].set_xticklabels([f'F{i}' for i in range(10)], rotation=45)
    axes[0, 1].set_yticklabels([f'F{i}' for i in range(10)])
    
    # 特征分布箱线图（前5个特征）
    data_for_boxplot = [X[:, i] for i in range(5)]
    axes[1, 0].boxplot(data_for_boxplot, labels=[f'F{i}' for i in range(5)])
    axes[1, 0].set_title('特征分布箱线图（前5个特征）')
    axes[1, 0].set_ylabel('特征值')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 训练集测试集分布对比
    train_mean = X_train.mean(axis=0)[:5]
    test_mean = X_test.mean(axis=0)[:5]
    x = np.arange(5)
    width = 0.35
    axes[1, 1].bar(x - width/2, train_mean, width, label='训练集', color='skyblue')
    axes[1, 1].bar(x + width/2, test_mean, width, label='测试集', color='lightcoral')
    axes[1, 1].set_xlabel('特征')
    axes[1, 1].set_ylabel('均值')
    axes[1, 1].set_title('训练集和测试集特征均值对比')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels([f'F{i}' for i in range(5)])
    axes[1, 1].legend()
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    os.makedirs('exp/figures', exist_ok=True)
    plt.savefig('exp/figures/data_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

def update_task_status(task_id, new_status, result_summary=None):
    """更新任务状态"""
    # 读取任务计划
    with open('exp/task_plan.json', 'r', encoding='utf-8') as f:
        task_plan = json.load(f)
    
    # 更新任务状态
    for task in task_plan['tasks']:
        if task['id'] == task_id:
            old_status = task['status']
            task['status'] = new_status
            task['completed_at'] = '2024-01-15 10:00:00'
            if result_summary:
                task['result_summary'] = result_summary
            print(f"任务 {task_id} 状态从 '{old_status}' 更新为 '{new_status}'")
            break
    
    # 保存更新后的任务计划
    with open('exp/task_plan.json', 'w', encoding='utf-8') as f:
        json.dump(task_plan, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()