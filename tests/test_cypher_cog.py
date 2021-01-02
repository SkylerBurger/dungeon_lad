import pytest

from discord.ext import commands

from cogs.cypher import CypherSystem


@pytest.fixture
def cypher():
    client = commands.Bot(command_prefix='/')
    return CypherSystem(client)


def test_roll_d20_in_range(cypher):
    rolls = [cypher.roll_d20() for _ in range(100)]
    assert all([0 < die < 21 for die in rolls])

def test_calculate_success_no_extras(cypher):
    expected = 2
    actual = cypher.calculate_success(7, 0, 0, 0)
    assert actual == expected

def test_calculate_success_with_extras(cypher):
    expected = 8
    actual = cypher.calculate_success(14, 2, 1, 1)
    assert actual == expected

def test_parse_cypher_variants(cypher):
    expected = (2, 1, 1, 1)
    actuals = []
    # In order
    actuals.append(cypher.parse_cypher('/cy effort 2 asset 1 bonus 1 shift 1')) 
    # Out of order
    actuals.append(cypher.parse_cypher('/cy bonus 1 effort 2 asset 1 shift 1'))
    # With plurals
    actuals.append(cypher.parse_cypher('/cy effort 2 assets 1 bonuses 1 shifts 1'))
    # With shorthand
    actuals.append(cypher.parse_cypher('/cy e 2 a 1 b 1 s 1'))
    assert all([actual == expected for actual in actuals])
