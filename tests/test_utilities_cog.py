from unittest.mock import Mock

import pytest

from discord.ext import commands

from cogs.utilities import Utilities


@pytest.fixture
def util():
    client = commands.Bot(command_prefix='/')
    return Utilities(client, 'tests/test_characters.json')

@pytest.fixture
def ctx():
    context = Mock()
    context.message.author = 'Skybur#5745'
    return context

def test_get_player_and_character(util, ctx):
    expected = ('Skybur#5745', 'Rune Amon')
    actual = util.get_player_and_character(ctx)
    assert actual == expected