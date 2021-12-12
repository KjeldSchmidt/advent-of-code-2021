from collections import defaultdict

connections = defaultdict(set)

with open("12-input.txt", "r") as f:
    for line in f.readlines():
        connection = line.strip().split("-")

        connections[connection[0]].add(connection[1])
        connections[connection[1]].add(connection[0])

print(connections)


def build_path(node: str, visited: set[str]) -> list[list[str]]:
    if node == "end":
        return [["end"]]

    visited = set(visited)
    visited.add(node)
    paths = []
    for neighbor in connections[node]:
        if neighbor in visited and not neighbor.isupper():
            continue

        new_paths = build_path(neighbor, visited)
        paths.extend([ [node] + path for path in new_paths])

    return paths


paths = build_path("start", set())
print("Solution part 1:")
print(len(paths))


def build_path2(node: str, visited: dict[str, int], double_visit_done: bool) -> list[list[str]]:
    if node == "end":
        return [["end"]]

    visited = {**visited}
    node_visit_count = visited.get(node, 0) + 1
    visited[node] = node_visit_count
    paths = []
    visit_limit = 0 if double_visit_done else 1
    for neighbor in connections[node]:
        if (visited.get(neighbor, 0) > visit_limit and not neighbor.isupper()) or neighbor == "start":
            continue

        new_double_visit_done = False
        if visited.get(neighbor, 0) == 1 and not neighbor.isupper():
            new_double_visit_done = True

        new_paths = build_path2(neighbor, visited, double_visit_done or new_double_visit_done)
        paths.extend([ [node] + path for path in new_paths])

    return paths


paths = build_path2("start", {}, False)
print("Solution part 2:")
print(len(paths))
