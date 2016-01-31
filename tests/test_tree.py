from hamcrest import assert_that, is_, instance_of, equal_to

from tree import Tree

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

def test_traverse_uses_depth_first_strategy():
    t = Tree('a')
    child = t.add_child('b')
    child.add_child('d')
    child.add_child('e')
    t.add_child('c')

    visited = []
    def visit_all(node):
        visited.append(node.value)
        return False

    t.traverse(visit_all)

    assert_that(visited, is_(['a', 'b', 'd', 'e', 'c']))

def test_find_returns_node_with_the_specified_value_when_such_exists():
    t = Tree('a')
    t.add_child('b')
    t.add_child('c').add_child('d').add_child('e')

    node = t.find('d')

    assert_that(node.children[0].value, is_('e'))
