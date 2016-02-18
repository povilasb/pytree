from hamcrest import assert_that, is_, equal_to

from tree import Tree

def make_tree_visitor(stop_for_value=None):
    """Contructs tree visitor predicate.
    """
    visited = []

    def visit_all(node):
        visited.append(node.value)
        if node.value == stop_for_value:
            return True
        return False

    return visit_all, visited

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

def test_traverse_uses_depth_first_strategy():
    t = make_test_tree()

    visit_all, visited = make_tree_visitor()
    t.traverse(visit_all)

    assert_that(visited, is_(['a', 'b', 'd', 'e', 'c']))

def test_find_returns_node_with_the_specified_value_when_such_exists():
    t = Tree('a')
    t.add_child('b')
    t.add_child('c').add_child('d').add_child('e')

    node = t.find('d')

    assert_that(node.children[0].value, is_('e'))

def test_traverse_breadth_calls_the_specified_predicate_only_for_root_node_when_it_has_no_children():
    t = Tree('a')

    visit_all, visited = make_tree_visitor()
    t.traverse_breadth_first(visit_all)

    assert_that(visited, is_(['a']))

def test_traverse_breadth_uses_breadth_first_strategy():
    t = make_test_tree()

    visit_all, visited = make_tree_visitor()
    t.traverse_breadth_first(visit_all)

    assert_that(visited, is_(['a', 'b', 'c', 'd', 'e']))

def test_traverse_breadth_stops_when_predicate_returns_true():
    t = make_test_tree()

    visit_all, visited = make_tree_visitor(stop_for_value='c')
    t.traverse_breadth_first(visit_all)

    assert_that(visited, is_(['a', 'b', 'c']))

def test_traverse_breadth_returns_current_node_for_which_predicate_returns_true():
    t = make_test_tree()

    visit_all, _ = make_tree_visitor(stop_for_value='c')
    found_node = t.traverse_breadth_first(visit_all)

    assert_that(found_node.value, is_('c'))

def test_traverse_breadth_returns_none_if_predicate_never_returns_true():
    t = make_test_tree()

    visit_all, _ = make_tree_visitor(stop_for_value=None)
    found_node = t.traverse_breadth_first(visit_all)

    assert_that(found_node, is_(None))
