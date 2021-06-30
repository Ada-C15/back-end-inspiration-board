from app.models.board import Board
from app.models.card import Card

############################ TEST /BOARDS ENDPOINT ############################

def test_get_all_boards_three_saved_boards(client, three_boards):
    #Act
    response = client.get("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "board_id": 1,
            "title": "Pick me up",
            "owner": "Simon"
        },
        {
            "board_id": 2,
            "title": "Cool plants",
            "owner": "Jamie"
        },
        {
            "board_id": 3,
            "title": "Travel destinations",
            "owner": "Alex"
        }
    ]

def test_get_all_boards_no_saved_boards(client):
    #Act
    response = client.get("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_one_saved_board(client, one_board):
    #Act
    response = client.get("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body.length == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "Healthy Habits",
            "owner": "Jose"
        }
    ]

def test_create_board(client):
    #Act
    response = client.post("/boards", json={
        "title": "New board!",
        "owner": "Maite"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "New board!",
            "owner": "Maite"
        }
    }

def test_create_board_missing_title(client):
    #Act
    response = client.post("/boards", json={
        "owner": "Johannes"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }

def test_create_board_missing_owner(client):
    #Act
    response = client.post("/boards", json={
        "title": "New board!",
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }


############################ TEST /BOARDS/{id} ENDPOINT ############################

def test_get_board(client, one_board):
    #Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Healthy Habits",
            "owner": "Jose"
        }
    }

def test_get_board_not_found(client):
    #Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404
    assert response_body == None

