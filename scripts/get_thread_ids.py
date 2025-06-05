import discord
from discord.ext import commands
import asyncio
import os
import json

async def get_forum_thread_ids(config):
    """获取论坛频道的所有线程ID"""
    intents = discord.Intents.default()
    intents.guilds = True
    
    bot = commands.Bot(
        command_prefix='!',
        intents=intents,
        proxy=config.get('proxy')
    )
    
    thread_ids = []
    
    @bot.event
    async def on_ready():
        print(f"Bot已登录: {bot.user}")
        nonlocal thread_ids
        
        try:
            channel = bot.get_channel(config['channel_id'])
            if not channel:
                print(f"错误：找不到ID为 {config['channel_id']} 的频道")
                await bot.close()
                return
                
            # 检查是否为论坛频道
            if not hasattr(channel, 'threads') or not isinstance(channel, discord.ForumChannel):
                print("错误：该频道不是论坛频道")
                await bot.close()
                return
                
            # 获取所有线程
            all_threads = []
            
            # 当前活动线程
            active_threads = channel.threads
            print(f"找到{len(active_threads)}个活动线程")
            all_threads.extend(active_threads)
            
            # 归档线程
            try:
                archived_threads = await channel.archived_threads(limit=None).flatten()
                print(f"找到{len(archived_threads)}个归档线程")
                all_threads.extend(archived_threads)
            except Exception as e:
                print(f"获取归档线程时出错: {str(e)} - 仅保存活动线程")
            
            # 收集线程ID
            thread_ids = [str(thread.id) for thread in all_threads]
            print(f"成功获取{len(thread_ids)}个线程ID")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await bot.close()
    
    await bot.start(config['bot_token'])
    return thread_ids

def save_thread_ids(thread_ids, output_file):
    """保存线程ID到文件"""
    with open(output_file, 'w') as f:
        f.write('\n'.join(thread_ids))
    print(f"线程ID已保存到 {output_file}")

if __name__ == "__main__":
    # 加载配置
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # 获取线程ID
    loop = asyncio.get_event_loop()
    thread_ids = loop.run_until_complete(get_forum_thread_ids(config))
    
    # 保存结果
    save_thread_ids(thread_ids, config['output_thread_ids'])
