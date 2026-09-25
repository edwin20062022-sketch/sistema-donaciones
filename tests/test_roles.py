def test_user_is_forbidden_from_admin_listing(client, user_token):
    assert client.get("/donantes", headers={"Authorization": f"Bearer {user_token}"}).status_code == 403


def test_admin_can_list_donors(client, admin_token):
    response = client.get("/donantes", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json() == []

