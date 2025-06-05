import subprocess
import time
import json
import os
import sys
from pathlib import Path

def export_threads(config):
    """导出所有线程"""
    # 创建输出目录
    output_dir = Path(config['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取线程ID
    with open(config['thread_ids_file'], 'r') as f:
        thread_ids = [line.strip() for line in f.readlines() if line.strip()]
    
    total = len(thread_ids)
    print(f"开始导出 {total} 个线程...")
    
    success_count = 0
    results = []
    
    for idx, thread_id in enumerate(thread_ids, 1):
        print(f"\n[进度 {idx}/{total}] 导出线程: {thread_id}")
        
        result = export_single_thread(thread_id, config, output_dir)
        results.append(result)
        
        if result['success']:
            print(f"✓ 成功导出线程 {thread_id}")
            success_count += 1
        else:
            print(f"✗ 导出失败: {result['message']}")
            
            # 添加详细错误分析
            if "Message Content Intent" in result['message']:
                print("⚠️ 解决方案:")
                print("1. 访问 https://discord.com/developers/applications")
                print("2. 选择你的应用")
                print("3. 转到'Bot'标签页")
                print("4. 启用'MESSAGE CONTENT INTENT'")
                print("5. 重置Token并使用新Token")
        
        # 进度百分比
        percent = int(idx * 100 / total)
        print(f"进度: {percent}%")
        
        # 延迟防止速率限制
        if idx < total:
            print(f"等待 {config['delay_seconds']} 秒...")
            time.sleep(config['delay_seconds'])
    
    print(f"\n导出完成! 成功导出 {success_count}/{total} 个线程")
    
    # 创建合并文件
    if success_count > 0:
        create_combined_file(output_dir, thread_ids)
    
    # 保存导出结果报告
    save_export_report(results, output_dir)
    
    return results

def export_single_thread(thread_id, config, output_dir):
    """导出单个线程"""
    output_file = output_dir / f"{thread_id}.json"
    cmd = [
        config['dce_path'],
        "export",
        "-t", config['bot_token'],
        "-c", thread_id,
        "-f", "Json",
        "-o", str(output_file),
        "--media"
    ]
    
    # 指定Token类型（如果配置了）
    if config.get('token_type'):
        cmd.extend(['--token-type', config['token_type']])
    
    env = os.environ.copy()
    if config.get('proxy'):
        env["HTTP_PROXY"] = config['proxy']
        env["HTTPS_PROXY"] = config['proxy']
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        return {
            'success': True,
            'thread_id': thread_id,
            'message': result.stdout,
            'output_file': str(output_file)
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'thread_id': thread_id,
            'message': f"错误代码: {e.returncode}\n错误信息: {e.stderr}",
            'output_file': None
        }

def create_combined_file(output_dir, thread_ids):
    """创建合并的JSON文件"""
    combined_data = []
    
    for thread_id in thread_ids:
        file_path = output_dir / f"{thread_id}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    combined_data.append({
                        "thread_id": thread_id,
                        "data": data
                    })
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {str(e)}")
    
    if combined_data:
        combined_file = output_dir / "combined_forum_backup.json"
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        print(f"已创建合并文件: {combined_file}")

def save_export_report(results, output_dir):
    """保存导出结果报告"""
    report_file = output_dir / "export_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"导出报告已保存到: {report_file}")

if __name__ == "__main__":
    try:
        # 加载配置
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # 执行导出
        export_threads(config)
    except Exception as e:
        print(f"发生未预期错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        input("\n按Enter键退出...")
