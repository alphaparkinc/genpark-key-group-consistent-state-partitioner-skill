import sys
import json
from client import KeyGroupPartitioner

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "route":
        p = KeyGroupPartitioner(params.get("max_groups", 64), params.get("workers", ["w1", "w2"]))
        return p.route_key(params.get("key", "test"))
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
