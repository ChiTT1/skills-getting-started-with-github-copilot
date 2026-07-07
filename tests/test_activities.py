from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success_and_404(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{quote(activity)}/signup"
    resp = client.post(url, params={"email": email})
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")

    # verify participant added
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity]["participants"]

    # non-existent activity -> 404
    resp3 = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert resp3.status_code == 404


def test_delete_participant_success_and_404(client):
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    delete_url = f"/activities/{quote(activity)}/participants"

    # successful delete
    resp = client.delete(delete_url, params={"email": existing_email})
    assert resp.status_code == 200
    assert existing_email in resp.json().get("message", "")

    # verify removed
    resp2 = client.get("/activities")
    assert existing_email not in resp2.json()[activity]["participants"]

    # deleting non-existent participant -> 404
    resp3 = client.delete(delete_url, params={"email": "noone@nowhere.com"})
    assert resp3.status_code == 404

    # deleting from non-existent activity -> 404
    resp4 = client.delete("/activities/DoesNotExist/participants", params={"email": "x@y.com"})
    assert resp4.status_code == 404


def test_static_index_and_root_redirect(client):
    # static index
    resp = client.get("/static/index.html")
    assert resp.status_code == 200
    assert "Mergington High School" in resp.text

    # root redirects to static index (don't follow redirects)
    resp2 = client.get("/", follow_redirects=False)
    assert resp2.status_code in (301, 302, 303, 307, 308)
    assert resp2.headers.get("location") == "/static/index.html"
