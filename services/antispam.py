import time
from collections import defaultdict, deque

MAX_MSG = 5      # số tin
WINDOW = 10      # giây

_user_msgs = defaultdict(deque)

def is_spam(psid: str) -> bool:
    now = time.time()
    q = _user_msgs[psid]

    while q and now - q[0] > WINDOW:
        q.popleft()

    q.append(now)
    return len(q) > MAX_MSG
