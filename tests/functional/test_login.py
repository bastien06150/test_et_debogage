def test_login_unknown_email_should_not_crash(client):
    response = client.post("/showSummary", data={"email": "fake@email.com"})

    # Le point clé : pas de 500
    assert response.status_code in (200, 302)
