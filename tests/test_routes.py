from app.models.board import Board

def test_get_board():
    #Act
    #Assert
# 200 response code to get board and body with appropriate board (id, title, owner, cards?)





# def test_get_task(client, one_task):
#     # Act
#     response = client.get("/tasks/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert "task" in response_body
#     assert response_body == {
#         "task": {
#             "id": 1,
#             "title": "Go on my daily walk 🏞",
#             "description": "Notice something new every day",
#             "is_complete": False
#         }
#     }