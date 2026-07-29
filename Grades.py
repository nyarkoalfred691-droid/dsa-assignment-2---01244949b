"""
Part D: Hash Tables and Binary Search Trees
ATU Student Grade Management Portal
"""


# ---------------------------------------------------------------------
# Section D1: Hash Tables
# ---------------------------------------------------------------------

def grade_frequency_report(results):
    """
    D2: Takes a list of (student_id, grade_letter) tuples and returns a
    dict mapping each of 'A','B','C','D','F' to the count of students
    who received it. Runs in O(N) time using a hash table (dict).
    """
    counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for _student_id, grade in results:
        if grade in counts:
            counts[grade] += 1
    return counts


def find_students_with_grade(results, grade):
    """
    D3: Returns a SORTED list of student_ids who received `grade`.
    Runs in O(N log N): building the matching list via a hash-based
    pass is O(N), but the final sort() is O(N log N), which dominates.
    The overall complexity is therefore NOT O(N) -- grouping with a
    hash table is fast, but producing a *sorted* result still requires
    a comparison sort over the matches.
    """
    matches = [sid for sid, g in results if g == grade]
    matches.sort()
    return matches


# ---------------------------------------------------------------------
# Section D2: Binary Search Trees
# ---------------------------------------------------------------------

class BSTNode:
    def __init__(self, student_id, grade_score):
        self.student_id = student_id
        self.grade_score = grade_score
        self.left = None
        self.right = None


def insert(root, student_id, grade_score):
    """
    D4: Recursively inserts a new node keyed on grade_score, following
    standard BST ordering (left = smaller, right = larger or equal).
    """
    if root is None:
        return BSTNode(student_id, grade_score)
    if grade_score < root.grade_score:
        root.left = insert(root.left, student_id, grade_score)
    else:
        root.right = insert(root.right, student_id, grade_score)
    return root


def inorder_traversal(root):
    """
    D5: Generator that yields (student_id, grade_score) pairs in
    ascending order of grade_score.

    In-order traversal (left, node, right) produces a sorted sequence
    in a BST because, by the BST invariant, every node in a subtree's
    left branch has a smaller key and every node in its right branch
    has a larger (or equal) key. Visiting left-subtree, then the node
    itself, then right-subtree at every level therefore always emits
    keys in non-decreasing order.
    """
    if root is not None:
        yield from inorder_traversal(root.left)
        yield (root.student_id, root.grade_score)
        yield from inorder_traversal(root.right)


def search(root, grade_score):
    """
    D6a: Returns the student_id of the node matching grade_score, or
    None if not found.
    Time complexity: O(H), where H is the tree height -- at each step
    we discard one whole subtree, so we do at most H comparisons.
    """
    node = root
    while node is not None:
        if grade_score == node.grade_score:
            return node.student_id
        elif grade_score < node.grade_score:
            node = node.left
        else:
            node = node.right
    return None


def find_range(root, low, high):
    """
    D6b: Returns a list of student_id values whose grade_score falls
    within the inclusive range [low, high], in ascending order.
    Time complexity: O(H + K), where H is the tree height (cost of
    descending to the range) and K is the number of nodes that fall
    inside the range (cost of visiting/collecting them). This is
    generally better than O(N) because whole subtrees entirely outside
    [low, high] are pruned and never visited.

    H = O(log N) when the tree is balanced (roughly equal numbers of
    nodes on each side at every level). H = O(N) in the worst case,
    when the tree has degenerated into a linked-list shape -- e.g. if
    scores were inserted in already-sorted order, every node only has
    a right child (or only a left child), so the tree has no branching.
    """
    result = []

    def helper(node):
        if node is None:
            return
        if low < node.grade_score:
            helper(node.left)
        if low <= node.grade_score <= high:
            result.append(node.student_id)
        if node.grade_score < high:
            helper(node.right)

    helper(root)
    return result


if __name__ == "__main__":
    print("D2: grade_frequency_report")
    results = [
        (1001, 'A'), (1002, 'B'), (1003, 'A'), (1004, 'C'),
        (1005, 'B'), (1006, 'A'), (1007, 'F'), (1008, 'B'),
        (1009, 'C'), (1010, 'A'),
    ]
    # Output: {'A': 4, 'B': 3, 'C': 2, 'D': 0, 'F': 1}
    print(" ", grade_frequency_report(results))

    print("\nD3: find_students_with_grade('A')")
    # Output: [1001, 1003, 1006, 1010]
    print(" ", find_students_with_grade(results, 'A'))

    print("\nD4-D6: BST demo")
    records = [(1001, 72), (1002, 55), (1003, 88),
               (1004, 60), (1005, 95), (1006, 48)]
    root = None
    for sid, score in records:
        root = insert(root, sid, score)

    print("  in-order (ascending score):")
    # Output:
    #   student 1006: 48
    #   student 1002: 55
    #   student 1004: 60
    #   student 1001: 72
    #   student 1003: 88
    #   student 1005: 95
    for sid, score in inorder_traversal(root):
        print(f"    student {sid}: {score}")

    print("  search(88) ->", search(root, 88))                # Output: 1003
    print("  search(100) ->", search(root, 100))              # Output: None
    print("  find_range(50, 90) ->", find_range(root, 50, 90))    # Output: [1002, 1004, 1001, 1003]
