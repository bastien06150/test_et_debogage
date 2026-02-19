def test_points_page_is_public(client):
    res = client.get("/points")
    assert res.status_code == 200
    assert b"Club Points" in res.data
