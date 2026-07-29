"""
Part C: Linked Lists, Stacks, and Queues
ATU Campus Shuttle Booking System
"""

from collections import deque


# ---------------------------------------------------------------------
# Section C1: Doubly Linked List
# ---------------------------------------------------------------------

class Booking:
    """C1: A single booking node in the doubly linked list."""

    def __init__(self, booking_id, student_name, destination):
        self.booking_id = booking_id
        self.student_name = student_name
        self.destination = destination
        self.next = None
        self.prev = None


class ShuttleList:
    """C1: Doubly linked list of Booking nodes with head and tail pointers."""

    def __init__(self):
        self.head = None
        self.tail = None

    def add_booking(self, booking_id, student_name, destination):
        """
        C2: Appends a new booking to the end of the list.
        Time complexity: O(1) because the tail pointer gives direct
        access to the last node. Without a tail pointer, this would be
        O(N) since we would have to walk the whole list to find the end.
        """
        node = Booking(booking_id, student_name, destination)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return node

    def cancel_booking(self, booking_id):
        """
        C3: Removes the node with the given booking_id from any position
        (head, tail, or middle), fixing neighbouring pointers.
        Returns True if removed, False if not found. O(N) to locate the
        node (must scan), O(1) to unlink it once found.
        """
        current = self.head
        while current is not None:
            if current.booking_id == booking_id:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # removing head

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev  # removing tail

                current.next = None
                current.prev = None
                return True
            current = current.next
        return False

    def find_and_swap(self, id1, id2):
        """
        C4: Locates the two nodes with the given IDs and swaps their
        DATA fields (booking_id, student_name, destination) rather than
        relinking next/prev pointers.

        Time complexity: O(N) to locate both nodes (single pass, or two
        scans in the worst case), O(1) to swap once found -> O(N) overall.

        Swapping data is preferred over relinking pointers because
        pointer relinking in a doubly linked list requires carefully
        handling up to 8 pointer updates (next/prev on both nodes and
        both sets of neighbours), plus special cases when the nodes are
        adjacent or are the head/tail. Swapping the three data fields is
        a simple, low-risk O(1) operation once the nodes are found.
        """
        node1 = node2 = None
        current = self.head
        while current is not None and (node1 is None or node2 is None):
            if current.booking_id == id1:
                node1 = current
            elif current.booking_id == id2:
                node2 = current
            current = current.next

        if node1 is None or node2 is None:
            return False

        (node1.booking_id, node1.student_name, node1.destination,
         node2.booking_id, node2.student_name, node2.destination) = (
            node2.booking_id, node2.student_name, node2.destination,
            node1.booking_id, node1.student_name, node1.destination,
        )
        return True

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        return " <-> ".join(
            f"[{n.booking_id}:{n.student_name}->{n.destination}]" for n in self
        )


# ---------------------------------------------------------------------
# Section C2: Stack and Queue Application
# ---------------------------------------------------------------------

class RouteHistory:
    """
    C5: Stack of route-change strings, backed by a Python list.
    push:      O(1) amortised (list append)
    pop_undo:  O(1) (list pop from the end)
    peek:      O(1) (index into the last element)
    """

    def __init__(self):
        self._stack = []

    def push(self, change):
        self._stack.append(change)

    def pop_undo(self):
        if not self._stack:
            return None
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            return None
        return self._stack[-1]


class BoardingQueue:
    """
    C6: FCFS boarding queue backed by collections.deque.
    join:       O(1) (append to the right end)
    board:      O(1) (popleft from the left end)
    peek_next:  O(1)
    size:       O(1)

    collections.deque is preferred over a plain Python list because a
    list is a dynamic array: removing from the FRONT (list.pop(0)) is
    O(N), since every remaining element must be shifted left one slot.
    deque is implemented as a doubly linked block structure, so both
    popleft() and append() run in O(1), making it the correct choice
    for a queue where students are removed from the front regularly.
    """

    def __init__(self):
        self._queue = deque()

    def join(self, student_name):
        self._queue.append(student_name)

    def board(self):
        if not self._queue:
            return None
        return self._queue.popleft()

    def peek_next(self):
        if not self._queue:
            return None
        return self._queue[0]

    def size(self):
        return len(self._queue)


if __name__ == "__main__":
    print("C1-C4: ShuttleList demo")
    shuttle = ShuttleList()
    shuttle.add_booking(1, "Ama", "Circle")
    shuttle.add_booking(2, "Kojo", "Madina")
    shuttle.add_booking(3, "Efua", "Achimota")
    # Output: [1:Ama->Circle] <-> [2:Kojo->Madina] <-> [3:Efua->Achimota]
    print("  after adds:", shuttle)

    shuttle.cancel_booking(2)
    # Output: [1:Ama->Circle] <-> [3:Efua->Achimota]
    print("  after cancel(2):", shuttle)

    shuttle.add_booking(4, "Yaw", "Tema")
    shuttle.find_and_swap(1, 4)
    # Output: [4:Yaw->Tema] <-> [3:Efua->Achimota] <-> [1:Ama->Circle]
    print("  after swap(1,4):", shuttle)

    print("\nC5: RouteHistory demo")
    history = RouteHistory()
    history.push("Route A -> Route B")
    history.push("Route B -> Route C")
    print("  peek:", history.peek())                # Output: Route B -> Route C
    print("  pop_undo:", history.pop_undo())        # Output: Route B -> Route C
    print("  pop_undo:", history.pop_undo())        # Output: Route A -> Route B
    print("  pop_undo (empty):", history.pop_undo())# Output: None

    print("\nC6: BoardingQueue demo")
    queue = BoardingQueue()
    queue.join("Ama")
    queue.join("Kojo")
    queue.join("Efua")
    print("  size:", queue.size())                  # Output: 3
    print("  peek_next:", queue.peek_next())        # Output: Ama
    print("  board:", queue.board())                # Output: Ama
    print("  board:", queue.board())                # Output: Kojo
    print("  size:", queue.size())                  # Output: 1
