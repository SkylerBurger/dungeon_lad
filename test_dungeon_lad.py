from dungeon_lad import (
    calculate_success,
    parse_cypher,
    roll_d20,
) 

def test_calculate_success_exists():
    assert calculate_success

def test_roll_d20_exists():
    assert roll_d20

def test_roll_d20_in_range():
    rolls = [roll_d20() for _ in range(100)]
    assert all([0 < die < 21 for die in rolls])

def test_calculate_success_no_extras():
    expected = 2
    actual = calculate_success(7, 0, 0, 0)
    assert actual == expected

def test_calculate_success_with_extras():
    expected = 8
    actual = calculate_success(14, 2, 1, 1)
    assert actual == expected

def test_parse_cypher_variants():
    expected = (2, 1, 1,)
    actual_1 = parse_cypher('/cypher effort 2 assets 1 bonus 1') 
    actual_2 = parse_cypher('/cypher bonus 1 effort 2 asset 1')
    assert actual_1 == expected
    assert actual_2 == expected 
