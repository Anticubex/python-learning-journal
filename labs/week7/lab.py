class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


# Stack Implementation (LIFO)
class Stack:
    def __init__(self):
        self.dummy = StackNode(None)
        self.head = self.dummy

    def push(self, item):
        new_node = StackNode(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.head is self.dummy:
            return None
        ret = self.head
        self.head = self.head.next
        return ret.data

    def is_empty(self):
        return self.head is self.dummy


# Elevator Ride Simulation (LIFO)
class ElevatorRide:
    def __init__(self):
        self.stack = Stack()  # Using custom Stack

    def board_guest(self, guest_name):
        self.stack.push(guest_name)

    def start_ride(self, capacity):
        print("\nElevator Ride Starting!")
        for _ in range(capacity):
            if self.stack.is_empty():
                break
            print(f"{self.stack.pop()} is exiting the ride!")
        print("Ride finished.\n")


class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.is_empty():
            self.front = new_node
        else:
            self.rear.next = new_node
        self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.front.data
        self.front = self.front.next
        self.size -= 1
        if self.is_empty():
            self.rear = None
        return data

    def __len__(self):
        return self.size


# Roller Coaster Ride Simulation (FIFO)
class RollerCoasterRide:
    def __init__(self):
        self.queue = Queue()  # Using custom Queue

    def join_queue(self, guest_name):
        self.queue.enqueue(guest_name)

    def start_ride(self, capacity):
        print("\nRoller Coaster Ride Starting!")
        for _ in range(capacity):
            if self.queue.is_empty():
                break
            print(f"{self.queue.dequeue()} is boarding the ride!")
        print("Ride is running!\n")


# Explicit Priority Queue Implementation (Min-Heap)
class PQNode:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority
        self.next = None


class PriorityQueue:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, data, priority):
        new_node = PQNode(data, priority)

        if self.is_empty() or priority < self.head.priority:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.priority <= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            temp = self.head
            self.head = self.head.next
            return temp.data


# VIP Ride Simulation (Priority Queue)
class VIPRide:
    def __init__(self):
        self.priority_queue = PriorityQueue()  # Using custom Priority Queue

    def add_guest(self, guest_name, priority):
        self.priority_queue.push(guest_name, priority)

    def start_ride(self, capacity):
        print("\nVIP Ride Starting!")
        for _ in range(capacity):
            if self.priority_queue.is_empty():
                break
            print(f"{self.priority_queue.pop()} is boarding!")
        print("VIP Ride is running!\n")


# Testing the system
if __name__ == "__main__":
    # Elevator Ride Test
    elevator = ElevatorRide()
    elevator.board_guest("Alice")
    elevator.board_guest("Bob")
    elevator.board_guest("Charlie")
    elevator.start_ride(2)
    elevator.start_ride(2)

    # Roller Coaster Ride Test
    roller_coaster = RollerCoasterRide()
    roller_coaster.join_queue("Dave")
    roller_coaster.join_queue("Eve")
    roller_coaster.join_queue("Frank")
    roller_coaster.start_ride(2)
    roller_coaster.start_ride(2)

    # VIP Ride Test
    vip_ride = VIPRide()
    vip_ride.add_guest("Grace", 2)  # Lower number = higher priority
    vip_ride.add_guest("Hank", 1)
    vip_ride.add_guest("Ivy", 3)
    vip_ride.start_ride(2)
    vip_ride.start_ride(2)
