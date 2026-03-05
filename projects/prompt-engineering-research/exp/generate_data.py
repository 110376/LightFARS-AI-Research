#!/usr/bin/env python3
"""生成模拟实验数据集"""

import json
import random

# 设置随机种子以保证可重复性
random.seed(42)

def generate_humaneval_dataset(n_samples=164):
    """生成模拟的 HumanEval 数据集"""
    dataset = []
    algorithms = ['sorting', 'searching', 'dynamic_programming', 'greedy', 'math', 'string', 'array', 'recursion']
    
    for i in range(n_samples):
        task_id = f"HumanEval/{i}"
        algorithm = random.choice(algorithms)
        
        # 根据算法类型生成不同复杂度的任务
        if algorithm in ['sorting', 'searching', 'array']:
            complexity = random.uniform(0.2, 0.5)
        elif algorithm in ['string', 'math', 'greedy']:
            complexity = random.uniform(0.4, 0.7)
        else:  # dynamic_programming, recursion
            complexity = random.uniform(0.6, 0.95)
        
        dataset.append({
            "task_id": task_id,
            "prompt": f"Implement a function to solve {algorithm} problem #{i}",
            "canonical_solution": f"def solution_{i}():\n    pass",
            "test": f"assert solution_{i}() == expected",
            "algorithm": algorithm,
            "complexity_score": round(complexity, 3),
            "difficulty": "easy" if complexity < 0.4 else "medium" if complexity < 0.7 else "hard"
        })
    
    return dataset

def generate_mbpp_dataset(n_samples=974):
    """生成模拟的 MBPP 数据集"""
    dataset = []
    categories = ['basic', 'intermediate', 'advanced']
    
    for i in range(n_samples):
        task_id = f"MBPP/{i}"
        category = random.choices(categories, weights=[0.4, 0.4, 0.2])[0]
        
        if category == 'basic':
            complexity = random.uniform(0.1, 0.4)
        elif category == 'intermediate':
            complexity = random.uniform(0.35, 0.65)
        else:
            complexity = random.uniform(0.6, 0.9)
        
        dataset.append({
            "task_id": task_id,
            "text": f"Solve programming problem #{i} in category {category}",
            "code": f"# Solution for problem {i}",
            "test_list": [f"test_case_{j}" for j in range(random.randint(3, 8))],
            "category": category,
            "complexity_score": round(complexity, 3),
            "difficulty": "easy" if complexity < 0.4 else "medium" if complexity < 0.7 else "hard"
        })
    
    return dataset

if __name__ == "__main__":
    # 生成数据集
    print("生成 HumanEval 模拟数据集...")
    humaneval_data = generate_humaneval_dataset(164)
    print(f"✓ 生成 {len(humaneval_data)} 个 HumanEval 任务")

    print("\n生成 MBPP 模拟数据集...")
    mbpp_data = generate_mbpp_dataset(974)
    print(f"✓ 生成 {len(mbpp_data)} 个 MBPP 任务")

    # 保存数据集
    with open('exp/data/processed/humaneval.json', 'w', encoding='utf-8') as f:
        json.dump(humaneval_data, f, indent=2, ensure_ascii=False)
    print("✓ 保存 HumanEval 数据集到 exp/data/processed/humaneval.json")

    with open('exp/data/processed/mbpp.json', 'w', encoding='utf-8') as f:
        json.dump(mbpp_data, f, indent=2, ensure_ascii=False)
    print("✓ 保存 MBPP 数据集到 exp/data/processed/mbpp.json")

    # 统计信息
    print("\n数据集统计:")
    print(f"HumanEval: {len(humaneval_data)} 任务")
    print(f"  - Easy: {sum(1 for d in humaneval_data if d['difficulty']=='easy')}")
    print(f"  - Medium: {sum(1 for d in humaneval_data if d['difficulty']=='medium')}")
    print(f"  - Hard: {sum(1 for d in humaneval_data if d['difficulty']=='hard')}")

    print(f"\nMBPP: {len(mbpp_data)} 任务")
    print(f"  - Easy: {sum(1 for d in mbpp_data if d['difficulty']=='easy')}")
    print(f"  - Medium: {sum(1 for d in mbpp_data if d['difficulty']=='medium')}")
    print(f"  - Hard: {sum(1 for d in mbpp_data if d['difficulty']=='hard')}")
