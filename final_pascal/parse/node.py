from abc import ABC, abstractmethod


class Node(ABC):
    def print(self,priority=1):
        pass


class IdentifierNode(Node):
    def __init__(self,operand):
        self.operand = operand

    def print(self,priority=1):
        return str(self.operand.get_value())


class RealNode(Node):
    def __init__(self,operand):
        self.operand = operand

    def print(self, priority=1):
        return str(self.operand.get_value())


class IntegerNode(Node):
    def __init__(self,operand):
        self.operand = operand

    def print(self, priority=1):
        return str(self.operand.get_value())


class BinaryOperationNode(Node):
    def __init__(self,operation,left,right):
        self.operation = operation
        self.left = left
        self.right = right

    def print(self, priority=1):
        tab = "    "
        right = self.right.print(priority+1)
        left = self.left.print(priority+1)
        return f"{self.operation.get_value()}\n" \
               f"{tab*priority}{left}\n" \
               f"{tab*priority}{right}"


class UnaryOperationNode(Node):
    def __init__(self,operation, operand):
        self.operation = operation
        self.operand = operand

    def print(self, priority=1):
        if isinstance(self.operand,Node):
            operand=self.operand.print()
        else:
            operand=self.operand.get_value()
        return f"{self.operation.get_value()}{operand}"