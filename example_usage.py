from client import KeyGroupPartitioner

def main():
    print("=== Testing Key-Group Partitioner ===")
    partitioner = KeyGroupPartitioner(max_key_groups=64, workers=["worker_A", "worker_B"])
    res1 = partitioner.route_key("tenant_999")
    print("Initial routing:", res1)
    assert res1['target_worker'] in ["worker_A", "worker_B"]

    print("Adding worker_C to scale cluster...")
    partitioner.add_worker("worker_C")
    res2 = partitioner.route_key("tenant_999")
    print("Post-scale routing:", res2)
    assert res2['target_worker'] in ["worker_A", "worker_B", "worker_C"]

    print("Key-Group Partitioner verified successfully!")

if __name__ == '__main__':
    main()
