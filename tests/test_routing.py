from stream.routing import matches

DRIVERS = {"Ravi": "bangalore.koramangala.*", "Priya": "bangalore.indiranagar.*",
           "Arjun": "bangalore.*.ride", "Meena": "bangalore.*.food",
           "Karthik": "chennai.tnagar.food", "Control": "bangalore.#"}


def who(key):
    return [d for d, p in DRIVERS.items() if matches(p, key)]


def test_d1_table():
    assert who("bangalore.koramangala.food") == ["Ravi", "Meena", "Control"]
    assert who("bangalore.indiranagar.ride") == ["Priya", "Arjun", "Control"]
    assert who("bangalore.whitefield.ride") == ["Arjun", "Control"]
    assert who("chennai.tnagar.food") == ["Karthik"]
    assert who("chennai.whitefield.ride") == []
    assert who("bangalore.koramangala") == ["Control"]
