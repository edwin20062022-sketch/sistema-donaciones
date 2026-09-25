def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_donor_crud_and_not_found(client, user_token, admin_token, donor_payload):
    created = client.post("/donantes", json=donor_payload, headers=auth(user_token))
    assert created.status_code == 201
    donor_id = created.json()["id"]
    assert client.get(f"/donantes/{donor_id}", headers=auth(user_token)).status_code == 200
    assert client.get("/donantes/999", headers=auth(user_token)).status_code == 404
    listed = client.get("/donantes", headers=auth(admin_token))
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    updated_payload = {**donor_payload, "nombre": "Banco Actualizado", "tipo": "empresa"}
    updated = client.put(f"/donantes/{donor_id}", json=updated_payload, headers=auth(admin_token))
    assert updated.status_code == 200
    assert updated.json()["nombre"] == "Banco Actualizado"
    assert client.delete(f"/donantes/{donor_id}", headers=auth(admin_token)).status_code == 204
    assert client.get(f"/donantes/{donor_id}", headers=auth(admin_token)).status_code == 404
    assert client.delete(f"/donantes/{donor_id}", headers=auth(admin_token)).status_code == 404


def test_user_cannot_update_or_delete(client, user_token, admin_token, donor_payload):
    donor_id = client.post("/donantes", json=donor_payload, headers=auth(user_token)).json()["id"]
    assert client.put(f"/donantes/{donor_id}", json=donor_payload, headers=auth(user_token)).status_code == 403
    assert client.delete(f"/donantes/{donor_id}", headers=auth(user_token)).status_code == 403


def test_donor_validation_and_unauthorized(client, user_token, donor_payload):
    assert client.post("/donantes", json={**donor_payload, "tipo": "invalid"}, headers=auth(user_token)).status_code == 422
    assert client.post("/donantes", json=donor_payload).status_code == 401
