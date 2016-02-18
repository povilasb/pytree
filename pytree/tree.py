"""Tree data structure.

NOTE: this module is "a good enough": it's far from complete implementation,
but has all the functionality needed at the moment.
"""

from Queue import Queue

class Tree(object):
    """Tree data structure.
    """

    def __init__(self, value):
        """Creates tree with the specified root node value.

        Args:
            value (any): root node value.
        """
        self.value = value

        self.children = []

    def add_child(self, value):
        """Append new child node to the tree.

        Creates new tree node with the specified value and appends it
        to the current tree child nodes list.

        Args:
            value (any): appended tree root node value.

        Returns:
            Tree: created Tree instance.
        """
        new_node = Tree(value)
        self.children.append(new_node)

        return new_node

    def find(self, value):
        """Find node in the tree by the specified value.

        Args:
            value (any): node value used to find the node instance in the tree.

        Returns:
            Tree: found node instace, None on failure.
        """
        return self.traverse(lambda node: node.value == value)

    def traverse(self, predicate):
        """Traverse tree and apply the specified predicate for each node.

        Traversing is continued until predicate returns True.

        Args:
            predicate (callable): def op(node) - unary function called with
                the traversing node passed as an argument. This function
                must return True when the desired requirements are met and we
                want to stop traversing.

        Returns:
            Tree: tree node for which the specified predicate returns True.
                None if no nodes satisfies the predicate.
        """
        if predicate(self):
            return self

        else:
            node = None
            for c in self.children:
                node = c.traverse(predicate)

            return node

    def traverse_breadth_first(self, predicate):
        """Traverses tree using breadth first search strategy.

        Applies the specified predicate for each traversed node.
        Stops when thre predicate returns true.

        Args:
            predicate (callable): same as in traverse().

        Returns:
            Tree: tree node for which the specified predicate returns True.
                None if no nodes satisfies the predicate.
        """
        nodes_to_visit = Queue()
        nodes_to_visit.put(self)

        while not nodes_to_visit.empty():
            current_node = nodes_to_visit.get()
            if predicate(current_node):
                return current_node

            for child in current_node.children:
                nodes_to_visit.put(child)
