import dash_bootstrap_components as dbc
from dash import html


def CardDeck(cards):
    def transform_cards(cards):
        return [cards[:5], cards[5:10]]

    cards_ = transform_cards(cards)

    return dbc.Container(
        list(
            dbc.Row(list(dbc.Col(card) for card in row), className="mb-3")
            for row in cards_
        ),
        fluid=True,
    )