import pytest

from dungeon_lad import DungeonLad

@pytest.fixture
def laddie():
    return DungeonLad()

def test_roll_d20_in_range(laddie):
    rolls = [laddie.roll_d20() for _ in range(100)]
    assert all([0 < die < 21 for die in rolls])

def test_calculate_success_no_extras(laddie):
    expected = 2
    actual = laddie.calculate_success(7, 0, 0, 0)
    assert actual == expected

def test_calculate_success_with_extras(laddie):
    expected = 8
    actual = laddie.calculate_success(14, 2, 1, 1)
    assert actual == expected

def test_parse_cypher_variants(laddie):
    expected = (2, 1, 1, 1)
    actual_1 = laddie.parse_cypher('/cypher effort 2 assets 1 bonus 1 shift 1') 
    actual_2 = laddie.parse_cypher('/cypher bonus 1 effort 2 asset 1 shift 1')
    assert actual_1 == expected
    assert actual_2 == expected 
