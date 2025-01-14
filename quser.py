import requests
import json

# 定义查询
query = {
    "query": """
    {
        User(func: uid(0x2894)) {  # 替换为实际的帖子 UID
            uid
            dgraph.type
            id
            pubkey
            content
            posts{
                uid
                id
                content
            }
            mentioned_by {
                uid
                dgraph.type
                pubkey
                name
                about
                picture
                nip05
                website
                lud16
            }
        }
    }
    """
}

# 发送 HTTP 请求
url = "http://144.126.138.135:8080/query"
url = "http://212.56.40.235:8080/query"

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(query))
    response.raise_for_status()  # 检查请求是否成功
    result = response.json()
    print(result)
    # 解析查询结果
    event = result.get("data", {}).get("User", [])
    if event:
        print("查询成功，返回的帖子及其提到的用户数据:")
        print(json.dumps(event, indent=2, ensure_ascii=False))
    else:
        print("查询成功，但未找到帖子数据。")
except Exception as e:
    print(f"查询失败: {e}")



# exit()
query = {
    "query": """
    {
        user(func: type(User)) {  # 替换为实际的帖子 UID
            uid
            dgraph.type
            id
            content
            name
            pubkey
            posts{
                uid
                dgraph.type
                content
                created_at
            }
        }
    }
    """
}

# 发送 HTTP 请求
url = "http://144.126.138.135:8080/query"
url = "http://212.56.40.235:8080/query"

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(query))
    response.raise_for_status()  # 检查请求是否成功
    result = response.json()
    print(result)
    # 解析查询结果
    edges = []
    users = []
    nodes = result.get("data", {}).get("user", [])
    if nodes:
        for node in nodes:
            uid = node.get("uid")
            node_type = node.get("dgraph.type")[0]
            pubkey = node.get("pubkey")
            created_at = node.get('created_at')
            content = node.get('content')

            one_user = {'id':uid, 'type':node_type, 'pubkey':pubkey, 'created_at':created_at, 'content':content }
            users.append(one_user)
            print(f"节点 UID: {uid}, 类型: {node_type}")
            for predicate, value in node.items():
                if predicate == 'posts':
                    for one_value in value:
                        print(f"边: {uid} -> {one_value['uid']}")
                        one_edge = {"id": f"{uid}_{one_value['uid']}", 'source':uid, 'target':one_value['uid'],'label':one_value['uid'], 'type':'post'}
                        edges.append(one_edge)
        print("查询成功，返回的帖子及其提到的用户数据:")
        print(edges)
        print(users)
        # print(json.dumps(nodes, indent=2, ensure_ascii=False))
    else:
        print("查询成功，但未找到帖子数据。")
except Exception as e:
    print(f"查询失败: {e}")
