from unittest.mock import AsyncMock

import json

import pytest

from discord.ext import commands

from cogs.utilities import Utilities


@pytest.fixture
def util():
    client = commands.Bot(command_prefix='/')
    return Utilities(client, 'tests/test_characters.json')


@pytest.fixture
def ctx():
    context = AsyncMock()
    context.message.author = 'Skybur#5745'
    return context


@pytest.fixture
def characters():
    with open('tests/test_characters.json', 'w') as file:
        json.dump('{"Skybur#5745": "Rune Amon"}', file)


def test_get_player_and_character(util, ctx, characters):
    expected = ('Skybur#5745', 'Rune Amon')
    actual = util.get_player_and_character(ctx)
    assert actual == expected


def test_save_characters(util):
    util.client.characters = {
        'Skybur#5745': 'Felix the Cat'
    }
    util.save_characters()
    with open('tests/test_characters.json') as file:
        actual = file.readlines()[0]
    with open('tests/test_characters.json', 'w') as file:
        character_dict = {
            'Skybur#5745': 'Rune Amon'
        }
        json.dump(character_dict, file)

    expected = '{"Skybur#5745": "Felix the Cat"}'

    assert actual == expected


@pytest.mark.asyncio
async def test_report_name(util, ctx):
    await util.report_name('Skybur#5745', 'Rune Amon', ctx)
    ctx.message.channel.send.assert_called_once_with(
        '**Skybur** is registered as **Rune Amon**'
    )


@pytest.mark.asyncio
async def test_report_no_name(util, ctx):
    await util.report_name('Skybur#5745', 'Skybur', ctx)
    ctx.message.channel.send.assert_called_once_with(
        '**Skybur** does not have a character name registered'
    )
