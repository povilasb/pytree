from hamcrest import assert_that, is_, equal_to
import pytest

from tree import Tree

class TreeVisitor:
    """Cllable predicate used to traverse tree.

    Use self.visited_nodes to test how nodes were visited.
    """
    def __init__(self, stop_for_value=None):
        """
        Args:
            stop_for_value (any): makes a predicate to return True when
                currently traversed node has this value.
        """
        self.visited_nodes = []
        self.stop_for_value = stop_for_value

    def __call__(self, node):
        """This method is applied for every visited tree node.

        Returns:
            bool: True if current node value matches the self.stop_for_value.
        """
        self.visited_nodes.append(node.value)
        return node.value == self.stop_for_value

@pytest.fixture()
def tree_visitor():
    return TreeVisitor()

def make_test_tree():
    """Constructs basic tree for tests.
    """
    t = Tree('a')
    child = t.add_child('b')
    child.add_child('d')
    child.add_child('e')
    t.add_child('c')

    return t

def test_constructor_sets_node_value():
    t = Tree('a')

    assert_that(t.value, is_('a'))

def test_add_child_adds_node_to_the_empty_child_list():
    t = Tree('a')

    t.add_child('b')

    assert_that(t.children[0].value, is_('b'))

def test_add_child_appends_node_to_the_child_list():
    t = Tree('a')
    t.add_child('b')

    t.add_child('c')

    assert_that(t.children[0].value, is_('b'))
    assert_that(t.children[1].value, is_('c'))

def test_add_child_returns_appended_node_instance():
    t = Tree('a')

    new_node = t.add_child('b')

    assert_that(new_node, equal_to(t.children[0]))

def test_traverse_returns_none_when_operation_always_returns_false():
    t = Tree('a')
    t.add_child('b')

    node = t.traverse(lambda n: False)

    assert_that(node, is_(None))

def test_traverse_returns_self_when_operation_returns_true_on_root_node():
    t = Tree('a')

    node = t.traverse(lambda n: True)

    assert_that(node, is_(t))

def test_traverse_uses_depth_first_strategy(tree_visitor):
    t = make_test_tree()

    t.traverse(tree_visitor)

    assert_that(tree_visitor.visited_nodes, is_(['a', 'b', 'd', 'e', 'c']))

def test_find_returns_node_with_the_specified_value_when_such_exists():
    t = Tree('a')
    t.add_child('b')
    t.add_child('c').add_child('d').add_child('e')

    node = t.find('d')

    assert_that(node.children[0].value, is_('e'))

def test_traverse_breadth_calls_the_specified_predicate_only_for_root_node_when_it_has_no_children(tree_visitor):
    t = Tree('a')

    t.traverse_breadth_first(tree_visitor)

    assert_that(tree_visitor.visited_nodes, is_(['a']))

def test_traverse_breadth_uses_breadth_first_strategy(tree_visitor):
    t = make_test_tree()

    t.traverse_breadth_first(tree_visitor)

    assert_that(tree_visitor.visited_nodes, is_(['a', 'b', 'c', 'd', 'e']))

def test_traverse_breadth_stops_when_predicate_returns_true(tree_visitor):
    t = make_test_tree()

    tree_visitor.stop_for_value = 'c'
    t.traverse_breadth_first(tree_visitor)

    assert_that(tree_visitor.visited_nodes, is_(['a', 'b', 'c']))

def test_traverse_breadth_returns_current_node_for_which_predicate_returns_true(tree_visitor):
    t = make_test_tree()

    tree_visitor.stop_for_value = 'c'
    found_node = t.traverse_breadth_first(tree_visitor)

    assert_that(found_node.value, is_('c'))

def test_traverse_breadth_returns_none_if_predicate_never_returns_true(tree_visitor):
    t = make_test_tree()

    tree_visitor.stop_for_value = None
    found_node = t.traverse_breadth_first(tree_visitor)

    assert_that(found_node, is_(None))
