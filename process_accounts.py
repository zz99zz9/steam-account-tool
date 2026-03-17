#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam账号处理脚本
1. 删除令牌目录里不在原始账号信息.txt中的令牌文件
2. 提取账号和密码到单独文档
"""

import os
import glob

# 使用当前目录
BASE_DIR = os.getcwd()
ACCOUNTS_FILE = os.path.join(BASE_DIR, "原始账号信息.txt")
TOKENS_DIR = os.path.join(BASE_DIR, "令牌")
OUTPUT_FILE = os.path.join(BASE_DIR, "账号密码.txt")

def read_account_list():
    """读取原始账号信息.txt，提取所有账号标识"""
    account_ids = set()
    account_passwords = []

    try:
        # 尝试多种编码
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']
        content = None

        for enc in encodings:
            try:
                with open(ACCOUNTS_FILE, 'r', encoding=enc) as f:
                    content = f.readlines()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            print("无法读取文件，尝试了多种编码都失败")
            return set(), []

        for line in content:
            line = line.strip()
            if not line:
                continue

            # 按 ---- 分割字段
            fields = line.split('----')
            if len(fields) >= 2:
                account_id = fields[0].strip()
                password = fields[1].strip()

                # 跳过空的账号
                if not account_id:
                    continue

                account_ids.add(account_id)
                account_passwords.append(f"{account_id}----{password}")

        print(f"从原始账号信息.txt中读取到 {len(account_ids)} 个账号")
        return account_ids, account_passwords

    except FileNotFoundError:
        print(f"错误: 找不到文件 {ACCOUNTS_FILE}")
        return set(), []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return set(), []


def clean_tokens_folder(valid_accounts):
    """删除不在有效账号列表中的令牌文件"""
    if not os.path.exists(TOKENS_DIR):
        print(f"错误: 令牌目录不存在 {TOKENS_DIR}")
        return

    # 获取所有.maFile文件
    mafile_pattern = os.path.join(TOKENS_DIR, "*.maFile")
    all_mafiles = glob.glob(mafile_pattern)

    deleted_count = 0
    kept_count = 0

    for mafile in all_mafiles:
        # 从文件名提取账号ID（去掉.maFile后缀）
        filename = os.path.basename(mafile)
        account_id = filename.replace('.maFile', '')

        if account_id not in valid_accounts:
            # 删除不在列表中的令牌文件
            os.remove(mafile)
            print(f"已删除令牌: {filename}")
            deleted_count += 1
        else:
            kept_count += 1

    print(f"\n清理完成: 保留 {kept_count} 个令牌, 删除 {deleted_count} 个令牌")


def save_account_passwords(account_passwords):
    """保存账号密码到单独文件"""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for entry in account_passwords:
                f.write(entry + '\n')

        print(f"\n账号密码已保存到: {OUTPUT_FILE}")
        print(f"共保存 {len(account_passwords)} 条记录")

    except Exception as e:
        print(f"保存文件时出错: {e}")


def main():
    print("=" * 50)
    print("Steam账号处理脚本")
    print("=" * 50)

    # 步骤1: 读取账号列表
    valid_accounts, account_passwords = read_account_list()

    if not valid_accounts:
        print("未找到有效账号，脚本退出")
        return

    # 步骤2: 清理令牌目录
    print("\n步骤1: 清理令牌目录")
    print("-" * 30)
    clean_tokens_folder(valid_accounts)

    # 步骤3: 保存账号密码
    print("\n步骤2: 提取账号密码")
    print("-" * 30)
    save_account_passwords(account_passwords)

    print("\n" + "=" * 50)
    print("处理完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
