#!/usr/bin/env python3
"""
Hungry Shrimp 贪吃虾对战 Agent
基于 https://hungryshrimp.coze.site/skill.md

用法:
  python3 hungry_shrimp.py [--api-key KEY] [--match-id ID] [--room-name NAME]

环境变量:
  AGENT_WORLD_API_KEY - Agent World API Key
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any

API_BASE = "https://hungryshrimp.coze.site/api/v1"

class HungryShrimpAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.match_id: Optional[str] = None
        
    def _request(self, method: str, path: str, data: Optional[Dict] = None) -> Dict:
        url = f"{API_BASE}{path}"
        headers = {
            "agent-auth-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        if data:
            body = json.dumps(data).encode("utf-8")
        else:
            body = None
            
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"HTTP Error {e.code}")
            return {"error": True, "code": e.code, "message": err_body[:200]}
        except Exception as e:
            print(f"Request failed: {e}")
            return {"error": True, "message": str(e)}
    
    def get_match(self, match_id: str) -> Dict:
        """获取比赛状态"""
        return self._request("GET", f"/matches/{match_id}")
    
    def submit_path(self, match_id: str, directions: List[str], reasoning: str = "") -> Dict:
        """提交移动路径"""
        return self._request("POST", f"/matches/{match_id}/path", {
            "directions": directions,
            "reasoning": reasoning
        })
    
    def get_lobby(self, status: str = "waiting") -> Dict:
        """获取大厅房间列表"""
        return self._request("GET", f"/lobby?status={status}")
    
    def create_room(self, name: str = "虾虾对战") -> Dict:
        """创建房间"""
        return self._request("POST", "/rooms", {"name": name})
    
    def join_room_by_name(self, name: str) -> Dict:
        """按名字加入房间"""
        return self._request("POST", "/rooms/join", {"name": name})
    
    def join_room_by_id(self, room_id: str) -> Dict:
        """按 ID 加入房间"""
        return self._request("POST", f"/rooms/{room_id}/join")
    
    def find_public_match(self) -> Optional[str]:
        """查找等待中的公开房间"""
        result = self.get_lobby("waiting")
        if "error" in result:
            return None
        
        rooms = result.get("data", {}).get("rooms", [])
        if rooms:
            return rooms[0].get("roomId")
        return None
    
    def calculate_safe_path(self, frame: Dict, my_id: str) -> List[str]:
        """
        简单策略：计算安全路径
        优先吃道具，避开墙壁和其他蛇
        """
        snakes = frame.get("snakes", [])
        items = frame.get("items", [])
        
        my_snake = None
        for s in snakes:
            if s.get("agentId") == my_id:
                my_snake = s
                break
        
        if not my_snake:
            return ["right"]  # 默认向右
        
        head = my_snake["body"][0]
        direction = my_snake.get("direction", "right")
        
        # 收集障碍物
        obstacles = set()
        for s in snakes:
            for segment in s["body"]:
                obstacles.add((segment["x"], segment["y"]))
        
        # 边界
        for x in range(-1, 51):
            obstacles.add((x, -1))
            obstacles.add((x, 50))
        for y in range(-1, 51):
            obstacles.add((-1, y))
            obstacles.add((50, y))
        
        # 优先找最近的食物
        target = None
        min_dist = float("inf")
        for item in items:
            pos = item.get("position", {})
            dist = abs(head["x"] - pos["x"]) + abs(head["y"] - pos["y"])
            priority = {"coin": 3, "food": 2, "shield": 1, "speed_boost": 0.5}.get(item["type"], 1)
            score = priority * 100 - dist
            if score > min_dist:
                min_dist = score
                target = pos
        
        # 生成路径
        path = []
        current = {"x": head["x"], "y": head["y"]}
        current_dir = direction
        
        for _ in range(10):
            safe_dirs = []
            for d in ["up", "down", "left", "right"]:
                # 避免 180 度掉头
                reverse_map = {"up": "down", "down": "up", "left": "right", "right": "left"}
                if reverse_map.get(current_dir) == d:
                    continue
                
                next_pos = self._move(current, d)
                if (next_pos["x"], next_pos["y"]) not in obstacles:
                    safe_dirs.append(d)
            
            if not safe_dirs:
                break
            
            # 选择方向
            if target:
                best_dir = self._choose_toward(current, target, safe_dirs)
            else:
                best_dir = safe_dirs[0]
            
            path.append(best_dir)
            current = self._move(current, best_dir)
            current_dir = best_dir
            
            if target and current["x"] == target["x"] and current["y"] == target["y"]:
                break
        
        return path if path else ["right"]
    
    @staticmethod
    def _move(pos: Dict, direction: str) -> Dict:
        moves = {
            "up": {"x": pos["x"], "y": pos["y"] - 1},
            "down": {"x": pos["x"], "y": pos["y"] + 1},
            "left": {"x": pos["x"] - 1, "y": pos["y"]},
            "right": {"x": pos["x"] + 1, "y": pos["y"]},
        }
        return moves.get(direction, pos)
    
    @staticmethod
    def _choose_toward(current: Dict, target: Dict, safe_dirs: List[str]) -> str:
        best = safe_dirs[0]
        best_dist = float("inf")
        for d in safe_dirs:
            next_pos = HungryShrimpAgent._move(current, d)
            dist = abs(next_pos["x"] - target["x"]) + abs(next_pos["y"] - target["y"])
            if dist < best_dist:
                best_dist = dist
                best = d
        return best
    
    def play(self, match_id: Optional[str] = None, room_name: Optional[str] = None):
        """
        主循环：参战或观战
        """
        if match_id:
            self.match_id = match_id
            print(f"加入比赛: {match_id}")
        elif room_name:
            print(f"加入房间: {room_name}")
            result = self.join_room_by_name(room_name)
            if "error" in result:
                print(f"加入失败: {result}")
                return
            self.match_id = result.get("data", {}).get("matchId")
            print(f"成功加入，比赛 ID: {self.match_id}")
        else:
            # 尝试加入等待中的房间
            found = self.find_public_match()
            if found:
                print(f"加入公开房间: {found}")
                result = self.join_room_by_id(found)
                if "error" not in result:
                    self.match_id = result.get("data", {}).get("matchId")
            else:
                # 创建新房间
                print("没有等待中的房间，创建新房间...")
                result = self.create_room("新道蓝谷 虾虾大作战")
                if "error" not in result:
                    self.match_id = result.get("data", {}).get("matchId")
                    print(f"创建房间成功，等待其他玩家加入...")
                    time.sleep(30)
                else:
                    print(f"创建房间失败: {result}")
                    return
        
        if not self.match_id:
            print("无法获取比赛 ID，退出")
            return
        
        # 预提交初始路径
        initial_path = ["right", "right", "right", "up", "up", "left", "left", "down", "down"]
        self.submit_path(self.match_id, initial_path, "初始探索路径")
        print(f"预提交初始路径: {initial_path}")
        
        # 主轮询循环
        tick_count = 0
        while True:
            result = self.get_match(self.match_id)
            
            if "error" in result:
                print("获取比赛状态失败，稍后重试")
                time.sleep(5)
                continue
            
            data = result.get("data", {})
            match = data.get("match", {})
            my_status = data.get("myStatus", {})
            frame = data.get("frame", {})
            
            status = match.get("status")
            current_tick = match.get("currentTick", 0)
            queue_depth = my_status.get("queueDepth", 0)
            is_alive = my_status.get("isAlive", False)
            my_id = my_status.get("agentId", "")
            
            print(f"[Tick {current_tick}] 队列深度: {queue_depth} | 存活: {is_alive} | 状态: {status}")
            
            if status == "finished":
                print("比赛结束")
                scoreboard = frame.get("scoreboard", [])
                for s in scoreboard:
                    print(f"  排名 {s.get('rankLive')}: {s.get('agentId')} - {s.get('score')} 分")
                break
            
            if not is_alive:
                print("已死亡，退出")
                break
            
            # 队列快空时提交新路径
            if queue_depth < 8:
                path = self.calculate_safe_path(frame, my_id)
                reasoning = f"寻找食物，当前方向 {frame.get('snakes', [{}])[0].get('direction', '?')}"
                resp = self.submit_path(self.match_id, path, reasoning)
                if resp.get("accepted"):
                    print(f"  提交路径: {path} (接受 {resp.get('acceptedCount')} 步)")
                else:
                    print(f"  提交失败: {resp.get('message', '未知错误')}")
            
            time.sleep(5)
            tick_count += 1
            
            # 安全退出
            if tick_count > 120:
                print("达到最大轮询次数，退出")
                break


def main():
    parser = argparse.ArgumentParser(description="Hungry Shrimp 贪吃虾对战 Agent")
    parser.add_argument("--api-key", help="Agent World API Key")
    parser.add_argument("--match-id", help="指定比赛 ID")
    parser.add_argument("--room-name", help="按名字加入房间")
    parser.add_argument("--watch", action="store_true", help="观战模式")
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("AGENT_WORLD_API_KEY")
    
    if not api_key:
        print("错误: 需要提供 Agent World API Key")
        print("获取方式:")
        print("  1. 访问 https://world.coze.site 注册")
        print("  2. 创建 Agent 获取 API Key")
        print("  3. 保存到 ~/.agent-world-key 或设置环境变量")
        print("  4. 或使用 --api-key 参数")
        sys.exit(1)
    
    agent = HungryShrimpAgent(api_key)
    agent.play(args.match_id, args.room_name)


if __name__ == "__main__":
    main()
