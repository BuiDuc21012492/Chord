import hashlib

class ChordNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.successor = None
        self.predecessor = None

    def __repr__(self):
        return f"Node({self.node_id})"


class Chord:
    def __init__(self, num_nodes=5, space_size=8):
        self.nodes = []
        self.circle = {}
        self.space_size = space_size  # Kích thước không gian băm
        self.max_id = 2 ** space_size
        self.num_nodes = num_nodes

    def hash(self, key):
        """ Hàm băm (hash function) để xác định khóa trong không gian băm """
        return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16) % self.max_id

    def add_node(self, node):
        """ Thêm nút vào hệ thống Chord """
        self.circle[node.node_id] = node
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.node_id)
        self._update_successors_and_predecessors()

    def _update_successors_and_predecessors(self):
        """ Cập nhật successor và predecessor cho tất cả các nút """
        for i, node in enumerate(self.nodes):
            node.predecessor = self.nodes[i - 1] if i > 0 else self.nodes[-1]
            node.successor = self.nodes[i + 1] if i + 1 < len(self.nodes) else self.nodes[0]

    def find_node(self, key):
        """ Tìm kiếm nút chịu trách nhiệm cho khóa """
        hashed_key = self.hash(key)
        print(f"Searching for key: {key} (hashed value: {hashed_key})")
        # Tìm nút có ID lớn hơn hoặc bằng giá trị băm của khóa
        for node in self.nodes:
            if node.node_id >= hashed_key:
                return node
        # Nếu không tìm thấy, quay lại nút đầu tiên trong vòng tròn
        return self.nodes[0]

    def display_ring(self):
        """ Hiển thị vòng tròn các nút """
        for node in self.nodes:
            print(f"Node {node.node_id} -> Predecessor: {node.predecessor.node_id} | Successor: {node.successor.node_id}")


# Test case
def test_chord():
    # Tạo hệ thống Chord với 5 nút
    chord = Chord(num_nodes=5)

    # Tạo các nút và thêm vào hệ thống
    for i in range(5):
        node = ChordNode(i)
        chord.add_node(node)

    # Hiển thị vòng tròn
    chord.display_ring()

    # Kiểm tra tìm kiếm cho khóa
    key_to_find = "7"
    responsible_node = chord.find_node(key_to_find)

    print(f"\nNode responsible for key {key_to_find}: {responsible_node}")


test_chord()
