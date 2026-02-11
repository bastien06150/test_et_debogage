def test_book_unknown_competition_or_club_should_not_crash(client):
    res = client.get("/book/FakeCompetition/FakeClub")
    assert res.status_code in (200, 302, 404)
    assert res.status_code != 500
