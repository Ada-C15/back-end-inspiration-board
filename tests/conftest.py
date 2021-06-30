import pytest
from app import create_app
from app import db
from app.models.card import Card
from app.models.board import Board


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(message="You can do it!")
    db.session.add(new_card)
    db.session.commit()

# This fixture creates three cards and saves them to the database.
@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(message="Rome, Italy"),
        Card(message="Christchurch, New Zealand"),
        Card(message="Johannesburg, South Africa")
    ])
    db.session.commit()

# This fixture creates a card with three likes.
@pytest.fixture
def one_card_with_three_likes(app):
    new_card = Card(message="I love you", likes_count=3)
    db.session.add(new_card)
    db.session.commit()

# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Healthy Habits",
                        owner="Jose")
    db.session.add(new_board)
    db.session.commit()

# This fixture creates a board and a card associated with that board.
@pytest.fixture
def one_card_belongs_to_one_board(app, one_goal, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()

# This fixture creates three boards and saves them to the database.
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(title="Pick me up", owner="Simon"),
        Board(title="Cool plants", owner="Jamie"),
        Board(title="Travel destinations", owner="Alex")
    ])
    db.session.commit()
