"""安全检查脚本 - 开源前检查敏感信息"""

import os
import re
import sys
import io
from pathlib import Path

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_secrets():
    """检查项目中是否包含敏感信息"""
    warnings = []

    # 检查的文件模式
    secret_patterns = [
        (r'sk-[a-zA-Z0-9]{32,}', 'API Key (sk-xxx)'),
        (r'ghp_[a-zA-Z0-9]{36,}', 'GitHub Token'),
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
        (r'password\s*=\s*["\'][^"\']+["\']', 'Password'),
        (r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']', 'API Key'),
    ]

    # 需要检查的目录
    check_dirs = ['src', 'config', 'projects']
    exclude_dirs = ['.git', '__pycache__', '.venv', 'venv']

    # 检查文件扩展名
    check_extensions = ['.py', '.md', '.txt', '.json', '.yml', '.yaml', '.env']

    print("[*] Checking for sensitive information...")
    print("=" * 60)

    for check_dir in check_dirs:
        dir_path = Path(check_dir)
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob('*'):
            # 跳过目录和排除的目录
            if file_path.is_dir():
                continue
            if any(excluded in str(file_path) for excluded in exclude_dirs):
                continue

            # 跳过 .env.example
            if file_path.name == '.env.example':
                continue

            # 只检查指定扩展名
            if file_path.suffix.lower() not in check_extensions:
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')

                for pattern, description in secret_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        warnings.append({
                            'file': str(file_path),
                            'type': description,
                            'matches': len(matches),
                            'pattern': pattern
                        })
            except Exception as e:
                pass

    # 输出结果
    if warnings:
        print(f"\n[!] Found {len(warnings)} potential sensitive information:\n")
        for warning in warnings:
            print(f"  File: {warning['file']}")
            print(f"     Type: {warning['type']}")
            print(f"     Matches: {warning['matches']}")
            print()
    else:
        print("[OK] No sensitive information found")

    # 检查 .gitignore 配置
    print("\n" + "=" * 60)
    print("[*] Checking .gitignore configuration...")
    print("-" * 60)

    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text(encoding='utf-8')

        required_ignores = [
            'config/.env',
            '*.env',
            '__pycache__',
            '*.log',
        ]

        all_good = True
        for required in required_ignores:
            if required not in gitignore_content:
                print(f"  [!] Recommended to add: {required}")
                all_good = False

        if all_good:
            print("  [OK] .gitignore is well configured")
    else:
        print("  [!] .gitignore file not found")

    # 检查是否有 .env 文件
    print("\n" + "=" * 60)
    print("[*] Checking environment configuration files...")
    print("-" * 60)

    env_files = list(Path('.').rglob('.env'))
    env_files = [f for f in env_files if f.name != '.env.example']

    if env_files:
        print(f"  [!] Found {len(env_files)} .env file(s):")
        for env_file in env_files:
            print(f"     - {env_file}")
        print("\n  [*] Make sure these files are NOT committed to GitHub!")
    else:
        print("  [OK] No .env files found")

    print("\n" + "=" * 60)
    print("[OK] Security check completed")
    print("=" * 60)

    # 返回是否有警告
    return len(warnings) == 0


if __name__ == "__main__":
    is_safe = check_secrets()

    if not is_safe:
        print("\n[!] Please handle the sensitive information before committing!")
        print("\nRecommended actions:")
        print("  1. Move API Keys to config/.env file")
        print("  2. Ensure .gitignore contains 'config/.env'")
        print("  3. Use 'git rm --cached' to remove committed sensitive files")
