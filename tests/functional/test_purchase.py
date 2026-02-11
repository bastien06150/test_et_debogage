def test_purchase_invalid_places_should_not_crash(client):
    res = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "abc",
        },
    )
    assert res.status_code != 500


def test_purchase_more_than_12_should_be_refused(client):
    res = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13",
        },
    )
    assert res.status_code != 500


def test_purchase_unknown_competition_or_club_should_not_crash(client):
    res = client.post(
        "/purchasePlaces",
        data={
            "competition": "FakeCompetition",
            "club": "FakeClub",
            "places": "1",
        },
    )
    assert res.status_code != 500
