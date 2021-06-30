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
    assert len(response_body) == 1
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
        "details": "invalid data"
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
        "details": "invalid data"
    }

def test_delete_boards(client, three_boards):
    #Act
    response = client.delete("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": "Boards successfully deleted"
    }
    assert Board.query.all() == []


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

def test_delete_board(client, three_boards):
    #Act
    response = client.delete("/boards/2")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 2 "Cool plants" successfully deleted'
    }
    assert len(Board.query.all()) == 2


############################ TEST /BOARDS/{id}/CARDS ENDPOINT ############################

def test_get_cards_for_specific_board():
    pass

def test_get_cards_for_nonexistant_board():
    pass

def test_post_new_card_to_board():
    pass

def test_post_new_card_to_board_missing_message():
    pass


################################## TEST /CARDS ENDPOINT #################################

def test_get_all_cards_three_saved_cards():
    pass

def test_get_all_cards_no_saved_cards():
    pass

def test_get_all_cards_one_saved_card():
    pass

def test_get_specific_card():
    pass

def test_get_specific_card_that_doesnt_exist():
    pass

def test_like_card():
    pass

def test_like_card_that_doesnt_exist():
    pass

def test_like_card_five_times():
    pass

def test_delete_card():
    pass

def test_delete_card_that_doesnt_exist():
    pass

################################# TEST QUERY PARAMETERS #################################

def test_get_boards_sort_by_title():
    pass

def test_get_boards_sort_by_owner():
    pass

def test_get_boards_filter_by_title():
    pass

def test_get_boards_filter_by_owner():
    pass

def test_get_boards_filter_by_owner_doesnt_exist():
    pass

def test_delete_boards_by_owner():
    pass

def test_delete_boards_by_title():
    pass

def test_delete_boards_by_owner_doesnt_exist():
    pass

