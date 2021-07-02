from app.models.board import Board
from app.models.card import Card


def test_get_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Test Board", 
            "owner": "pinspiration"
        }
    ]

def test_get_board_not_found(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None


def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "Test Board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details":"Invalid data error: please include title and owner information"}
    assert Board.query.all() == []


def test_get_card_for_a_specific_board(client, one_board_with_cards):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{'board_id': 1, 'card_id': 1, 'likes_count': 0, 'message': 'Test Message 1'},{
        'board_id': 1, 'card_id': 2, 'likes_count': 0, 'message': 'Test Message 2'} ]


def test_create_card_message_too_long(client):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "aaaaaaaaaabbbbbbbbbbbccccccccccdddddddddd000"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {"details":"please keep the message below 40 characters"}