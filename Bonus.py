"""
Part E (Bonus): Exam Invigilation Scheduler
"""


def build_conflict_map(sessions):
    """
    E1: Returns a dict mapping each room_id to a list of (i, j) index
    pairs (i < j) whose sessions conflict, where sessions[i] and
    sessions[j] share a room and start[j] < end[i].

    Approach: group session indices by room (O(N) using a hash table),
    then for each room compare every pair of its sessions (naive
    nested loop, O(M^2) per room of size M).
    """
    rooms = {}
    for idx, (room_id, _start, _end) in enumerate(sessions):
        rooms.setdefault(room_id, []).append(idx)

    conflict_map = {}
    for room_id, indices in rooms.items():
        conflicts = []
        for a in range(len(indices)):
            i = indices[a]
            for b in range(a + 1, len(indices)):
                j = indices[b]
                start_i, end_i = sessions[i][1], sessions[i][2]
                start_j, end_j = sessions[j][1], sessions[j][2]
                if i < j:
                    if start_j < end_i:
                        conflicts.append((i, j))
                else:
                    if start_i < end_j:
                        conflicts.append((j, i))
        conflict_map[room_id] = conflicts
    return conflict_map


def detect_first_conflict(room_sessions):
    """
    E2: room_sessions is a list of (index, start, end) tuples for a
    SINGLE room, already sorted by start time. Uses a stack to track
    the currently "open" session and returns the first conflicting
    pair of indices found, or None.

    Because the sessions are processed in start-time order, we only
    ever need to compare each new session against the one on top of
    the stack: if the new session starts before the top one ends, they
    conflict. Otherwise the top session is finished and can be popped
    (replaced by the new session as the current "open" one).
    """
    stack = []
    for idx, start, end in room_sessions:
        if stack:
            top_idx, _top_start, top_end = stack[-1]
            if start < top_end:
                return (top_idx, idx)
            else:
                stack.pop()
        stack.append((idx, start, end))
    return None


if __name__ == "__main__":
    sessions = [
        ('R1', 8, 10),   # index 0
        ('R1', 9, 11),   # index 1 -- conflicts with 0
        ('R1', 11, 13),  # index 2 -- no conflict with 1
        ('R2', 8, 12),   # index 3
        ('R2', 10, 14),  # index 4 -- conflicts with 3
    ]

    print("E1: build_conflict_map")
    # Output: {'R1': [(0, 1)], 'R2': [(3, 4)]}
    print(" ", build_conflict_map(sessions))

    print("\nE2: detect_first_conflict for room R1")
    r1_sessions = [(0, 8, 10), (1, 9, 11), (2, 11, 13)]
    # Output: (0, 1)
    print(" ", detect_first_conflict(r1_sessions))

    print("\nE2: detect_first_conflict for room R2")
    r2_sessions = [(3, 8, 12), (4, 10, 14)]
    # Output: (3, 4)
    print(" ", detect_first_conflict(r2_sessions))
