import nommor

quest_list = {
    1: {
        'name': 'ghosts hunt',
        'description': 'kill 5 ghosts',
        'objective': {
            'type': 'kill',        # kill, collect 등
            'target': 'ghost',
            'count': 5
        },
        'reward': {
            'exp': 100,
            'money': 304
        }
    },

    2: {
        'name': 'yetis hunt',
        'description': 'kill 8 yetis',
        'objective': {
            'type': 'kill',
            'target': 'yeti',
            'count': 3
        },
        'reward': {
            'exp': 400,
            'money': 1400
        }
    },
    3: {
        'name': 'wolf hunt',
        'description': 'kill 1 wolf',
        'objective': {
            'type': 'kill',
            'target': 'wolf',
            'count': 1
        },
        'reward': {
            'exp': 1500,
            'money': 10000
        }
    },
    4: {
        'name': 'forest tree gather',
        'description': 'collect 5 forest trees',
        'objective': {
            'type': 'collect',
            'target': 'forest_tree',
            'count': 5
        },
        'reward': {
            'exp': 800,
            'money': 5000
        }
    },
    5: {
        'name': 'snow tree gather',
        'description': 'collect 2 snow trees',
        'objective': {
            'type': 'collect',
            'target': 'snow_tree',
            'count': 2
        },
        'reward': {
            'exp': 800,
            'money': 5000,
            'double_jump' : True
        }
    },
    6: {
        'name': 'desert tree gather',
        'description': 'collect 5 desert trees',
        'objective': {
            'type': 'collect',
            'target': 'desert_tree',
            'count': 5
        },
        'reward': {
            'exp': 8000,
            'money': 5000
        }
    },
    7: {
        'name': 'snow tree gather',
        'description': 'collect 2 snow trees',
        'objective': {
            'type': 'collect',
            'target': 'snow_tree',
            'count': 4
        },
        'reward': {
            'exp': 800,
            'money': 5000,
            'double_jump' : True
        }
    }
}

quest_count = len(quest_list)

player_quest = {
    'available': [i+1 for i in range(quest_count)],     # 받을 수 있는 퀘스트 id
    'active': {},        # 진행 중인 퀘스트: {퀘스트ID: 현재 진행 수}
    'completed': []      # 완료한 퀘스트 id
}

def start_quest(quest_id):
    global player_quest, quest_list
    if quest_id in player_quest['available']:
        player_quest['available'].remove(quest_id)
        player_quest['active'][quest_id] = 0
        print(f"퀘스트 {quest_id} 시작!")


def update_quest(target):
    """몬스터 처치/아이템 획득 시 호출"""
    global player_quest, quest_list

    # 진행 중인 퀘스트만 순회 (복사본 사용 - 딕셔너리 수정 중 순회 오류 방지)
    for qid in list(player_quest['active'].keys()):
        obj = quest_list[qid]['objective']

        # 타입과 대상이 일치하는지 확인
        if obj['target'] == target:
            player_quest['active'][qid] += 1
            current = player_quest['active'][qid]
            required = obj['count']

            print(f"[{quest_list[qid]['name']}] 진행: {current}/{required}")

            # 완료 체크
            if current >= required:
                finish_quest(qid)

def finish_quest(quest_id):
    global player_quest, quest_list
    reward = quest_list[quest_id]['reward']
    print(f"퀘스트 '{quest_list[quest_id]['name']}' 완료!")
    print(f"보상: exp {reward['exp']}, 돈 {reward['money']}")
    if reward['double_jump']:
        print("보상: 더블 점프 능력 획득!")
        nommor.viego.can_double_jump = True

    # 상태 업데이트
    player_quest['completed'].append(quest_id)
    del player_quest['active'][quest_id]