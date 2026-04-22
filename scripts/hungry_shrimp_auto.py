#!/usr/bin/env python3
"""
x-valley hungry-shrimp 自动参战脚本
整合 Agent World 注册 + Hungry Shrimp 参战
"""
import os, sys, re, time, json, uuid, urllib.request, urllib.error

AGENT_WORLD_API = "https://world.coze.site/api"
HUNGRY_SHRIMP_API = "https://hungryshrimp.coze.site/api/v1"
KEY_FILE = os.path.expanduser("~/.agent-world-key")

WORD_MAP = {
    'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,
    'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,
    'eighteen':18,'nineteen':19,'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,
    'seventy':70,'eighty':80,'ninety':90,'hundred':100,'thousand':1000
}

def aw_req(path, data=None, auth=None):
    url = f"{AGENT_WORLD_API}{path}"
    h = {"Content-Type":"application/json"}
    if auth: h["agent-auth-api-key"] = auth
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=h, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error":True,"code":e.code,"msg":e.read().decode()[:200]}
    except Exception as e:
        return {"error":True,"msg":str(e)}

def hs_req(path, data=None, api_key=None):
    url = f"{HUNGRY_SHRIMP_API}{path}"
    h = {"agent-auth-api-key":api_key,"Content-Type":"application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=h, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:300]
        try:
            return json.loads(err)
        except:
            return {"error":True,"code":e.code,"msg":err}
    except Exception as e:
        return {"error":True,"msg":str(e)}

def solve_challenge(text):
    clean = re.sub(r'[^a-zA-Z0-9\s\-]',' ',text).lower()
    vals = []
    for t in re.findall(r'\b[a-z]+\b|\b\d+\b',clean):
        if t.isdigit(): vals.append(int(t))
        elif t in WORD_MAP: vals.append(WORD_MAP[t])
    if len(vals)<1: return 0
    if len(vals)==1: return vals[0]
    if any(w in clean for w in ['add','plus','more','total','together','sum','adds']):
        return sum(vals)
    if any(w in clean for w in ['subtract','minus','less','remove']):
        return vals[0]-sum(vals[1:])
    if any(w in clean for w in ['multiply','times','product']):
        p=1
        for v in vals: p*=v
        return p
    return sum(vals)

def ensure_api_key():
    key = None
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f: key = f.read().strip()
    if not key: key = os.environ.get("AGENT_WORLD_API_KEY")
    if key: return key
    print("未找到 API Key，自动注册 Agent World...")
    uname = f"xindao-{uuid.uuid4().hex[:8]}"
    r = aw_req("/agents/register", {"username":uname,"nickname":"新道蓝谷","bio":"金帝·新道蓝谷生命科学园"}, auth=None)
    if not r.get("success"): sys.exit(f"注册失败: {r.get('message','?')}")
    d = r["data"]
    key = d["api_key"]
    ans = solve_challenge(d["verification"]["challenge_text"])
    v = aw_req("/agents/verify", {"verification_code":d["verification"]["verification_code"],"answer":str(ans)}, auth=None)
    if not v.get("success"): sys.exit(f"验证失败: {v.get('message','?')}")
    with open(KEY_FILE,"w") as f: f.write(key)
    os.chmod(KEY_FILE,0o600)
    print(f"注册成功，key 已保存到 {KEY_FILE}")
    return key

def find_and_join(api_key):
    # 先检查是否已在某个房间中
    me = hs_req("/me", api_key=api_key)
    if "error" not in me:
        current_room = me.get("data",{}).get("agent",{}).get("currentRoomId")
        if current_room:
            print(f"已在房间中: {current_room}")
            room_detail = hs_req(f"/rooms/{current_room}", api_key=api_key)
            r = room_detail.get("data",{}).get("room",{})
            rname = r.get("name", "未知")
            print(f"房间: {rname} ({r.get('currentAgents',0)}/{r.get('maxAgents',0)}人)")
            return current_room, rname, None
    
    # 查找等待中的房间
    lobby = hs_req("/lobby?status=waiting", api_key=api_key)
    if "error" in lobby: return None, None, f"大厅失败: {lobby.get('message', lobby.get('msg','?'))}"
    rooms = lobby.get("data",{}).get("cards",[])
    
    # 尝试加入第一个未满的房间
    for room in rooms:
        rid, rname = room["roomId"], room["name"]
        occupied = room.get("occupiedAgents", 0)
        max_agents = room.get("maxAgents", 4)
        if occupied >= max_agents:
            print(f"房间 {rname} 已满 ({occupied}/{max_agents})，跳过")
            continue
        print(f"找到房间: {rname} ({rid}) {occupied}/{max_agents}")
        j = hs_req("/rooms/join", {"name":rname}, api_key)
        if "error" in j:
            err_msg = j.get("message", j.get("msg","")).lower()
            if "already" in err_msg or "in room" in err_msg:
                print("已在其他房间，尝试离开...")
                me = hs_req("/me", api_key=api_key)
                current_room = me.get("data",{}).get("agent",{}).get("currentRoomId") if "error" not in me else None
                if current_room:
                    hs_req(f"/rooms/{current_room}/leave", api_key=api_key)
                    time.sleep(1)
                j = hs_req("/rooms/join", {"name":rname}, api_key)
                if "error" in j: 
                    print(f"加入失败: {j.get('message', j.get('msg','?'))}，尝试下一个房间")
                    continue
            else:
                print(f"加入失败: {j.get('message', j.get('msg','?'))}，尝试下一个房间")
                continue
        print(f"加入成功!")
        return rid, rname, None
    
    # 所有房间都满或加入失败，创建新房间
    print("无可用房间，创建新房间...")
    r = hs_req("/rooms", {"name":"新道蓝谷 虾虾大作战"}, api_key)
    if "error" in r: return None, None, f"创建失败: {r.get('message', r.get('msg','?'))}"
    rid = r["data"]["room"]["id"]
    rname = r["data"]["room"]["name"]
    print(f"创建成功 {rid}，等待其他人...")
    return rid, rname, None

def calc_path(frame, my_id):
    snakes = frame.get("snakes",[])
    items = frame.get("items",[])
    me = next((s for s in snakes if s.get("agentId")==my_id), None)
    if not me: return ["right"]
    head = me["body"][0]
    direction = me.get("direction","right")
    obs = set()
    for s in snakes:
        for seg in s["body"]: obs.add((seg["x"],seg["y"]))
    for x in range(-1,51): obs.add((x,-1)); obs.add((x,50))
    for y in range(-1,51): obs.add((-1,y)); obs.add((50,y))
    target=None; best=-999
    for it in items:
        p=it.get("position",{})
        d=abs(head["x"]-p["x"])+abs(head["y"]-p["y"])
        s=(10 if it["type"]=="coin" else 5)*10-d
        if s>best: best=s; target=p
    path=[]; cur={"x":head["x"],"y":head["y"]}; cd=direction
    rev={"up":"down","down":"up","left":"right","right":"left"}
    move={"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}
    for _ in range(10):
        safe=[]
        for d in ["up","down","left","right"]:
            if rev.get(cd)==d: continue
            np=(cur["x"]+move[d][0], cur["y"]+move[d][1])
            if np not in obs: safe.append(d)
        if not safe: break
        if target:
            best=safe[0]; bd=999
            for d in safe:
                np={"x":cur["x"]+move[d][0],"y":cur["y"]+move[d][1]}
                dst=abs(np["x"]-target["x"])+abs(np["y"]-target["y"])
                if dst<bd: bd=dst; best=d
            d=best
        else: d=safe[0]
        path.append(d); cur["x"]+=move[d][0]; cur["y"]+=move[d][1]; cd=d
        if target and cur["x"]==target["x"] and cur["y"]==target["y"]: break
    return path if path else None

def wait_for_match(room_id, room_name, api_key):
    print(f"⏳ 等待比赛开始...")
    for i in range(60):
        room = hs_req(f"/rooms/{room_id}", api_key=api_key)
        r = room.get("data",{}).get("room",{})
        mid = r.get("currentMatchId")
        if mid:
            print(f"🎮 比赛开始! matchId={mid}")
            return mid
        st = r.get("status")
        ca = r.get("currentAgents", 0)
        ma = r.get("maxAgents", 4)
        if st == "countdown":
            print(f"  ⏱️ 倒计时 {r.get('countdownSeconds','?')}s")
        elif i % 5 == 0:
            print(f"  [{i}] {ca}/{ma}人 等待中...")
        time.sleep(2)
    return None

def play(match_id, api_key):
    print(f"\n🎮 参战: {match_id}")
    hs_req(f"/matches/{match_id}/path", {"directions":["right","right","up","up","left","left","down","down","right"],"reasoning":"初始探索"}, api_key)
    print("✅ 预提交初始路径")
    my_id = None
    for _ in range(120):
        r = hs_req(f"/matches/{match_id}", api_key=api_key)
        if "error" in r:
            print(f"  ⚠️ 获取状态失败: {r.get('msg','?')}")
            time.sleep(5); continue
        d=r.get("data",{})
        m=d.get("match",{}) or {}
        ms=d.get("myStatus",{}) or {}
        f=d.get("frame",{}) or {}
        st=m.get("status"); ct=m.get("currentTick",0); qd=ms.get("queueDepth",0) if ms else 0
        alive=ms.get("isAlive",False) if ms else False
        if my_id is None: my_id=ms.get("agentId","") if ms else ""
        print(f"[Tick {ct}] 队列:{qd} 存活:{'✅' if alive else '💀' if ms else '?'} 状态:{st}")
        if st=="finished":
            print("\n🏁 比赛结束!")
            sb=f.get("scoreboard",[])
            for s in sb:
                rank=s.get("rankLive","?"); name=s.get("nickname",s.get("agentId","?")[:8]); score=s.get("score",0)
                print(f"  #{rank}: {name} - {score}分{' ← 🦐 你' if s.get('agentId')==my_id else ''}")
            me=next((s for s in sb if s.get("agentId")==my_id),None)
            return True, f"排名 {me.get('rankLive','?') if me else '?'}，得分 {me.get('score',0) if me else 0}"
        if ms and not alive:
            print("\n💀 已死亡"); return True,"已死亡"
        if qd<8 and ms:
            p=calc_path(f,my_id)
            if p:
                rr=hs_req(f"/matches/{match_id}/path", {"directions":p,"reasoning":"寻找食物"}, api_key)
                print(f"  ➡️ {p} {'✅' if rr.get('accepted') else '❌'} {rr.get('message','')[:60]}")
        time.sleep(5)
    return True,"轮询结束"

def main():
    print("="*50+"\n🦐 新道蓝谷 × Hungry Shrimp\n"+"="*50)
    key = ensure_api_key()
    rid, rname, msg = find_and_join(key)
    if not rid: print(f"❌ {msg}"); sys.exit(1)
    mid = wait_for_match(rid, rname, key)
    if not mid: print("❌ 等待比赛超时"); sys.exit(1)
    ok, res = play(mid, key)
    print(f"\n{'✅' if ok else '❌'} {res}")

if __name__=="__main__": main()
