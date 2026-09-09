import hashlib

class KeyGroupPartitioner:
    """Key-group based state partitioner for elastic stream processing."""
    def __init__(self, max_key_groups=128, workers=None):
        self.max_key_groups = max_key_groups
        self.workers = list(workers) if workers else []
        self.worker_ranges = {}
        self.rebalance()

    def add_worker(self, worker_id):
        if worker_id not in self.workers:
            self.workers.append(worker_id)
            self.rebalance()

    def remove_worker(self, worker_id):
        if worker_id in self.workers:
            self.workers.remove(worker_id)
            self.rebalance()

    def rebalance(self):
        n = len(self.workers)
        if n == 0:
            self.worker_ranges = {}
            return
        self.workers.sort()
        groups_per_worker = self.max_key_groups // n
        remainder = self.max_key_groups % n

        current_idx = 0
        for i, w in enumerate(self.workers):
            count = groups_per_worker + (1 if i < remainder else 0)
            self.worker_ranges[w] = (current_idx, current_idx + count - 1)
            current_idx += count

    def get_key_group(self, key):
        h = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        return h % self.max_key_groups

    def route_key(self, key):
        kg = self.get_key_group(key)
        for w, (start, end) in self.worker_ranges.items():
            if start <= kg <= end:
                return {'key': key, 'key_group': kg, 'target_worker': w}
        return None
