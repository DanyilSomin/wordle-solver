from wordle_matcher import WordleMatcher

def run_tests():
    def test(secret, guess, expected):
        matcher = WordleMatcher(secret)
        result = matcher.match(guess)
        assert result == expected, f"FAIL: {secret=} {guess=} => {result} != {expected}"

    test("apple", "apple", ['G', 'G', 'G', 'G', 'G'])
    test("apple", "storm", ['B', 'B', 'B', 'B', 'B'])
    test("stone", "onest", ['Y', 'Y', 'Y', 'Y', 'Y'])
    test("stone", "stamp", ['G', 'G', 'B', 'B', 'B'])
    test("stone", "scent", ['G', 'B', 'Y', 'G', 'Y'])
    test("plant", "altar", ['Y', 'G', 'Y', 'B', 'B'])
    test("plant", "allay", ['Y', 'G', 'B', 'B', 'B'])
    test("press", "camps", ['B', 'B', 'B', 'Y', 'G'])
    test("level", "elevs", ['Y', 'Y', 'Y', 'Y', 'B'])
    test("sassy", "spasm", ['G', 'B', 'Y', 'G', 'B'])
    test("bobby", "bobby", ['G', 'G', 'G', 'G', 'G'])
    test("spike", "eerie", ['B', 'B', 'B', 'Y', 'G'])
    test("abbey", "babay", ['Y', 'Y', 'G', 'B', 'G'])
    test("babes", "bbbbb", ['G', 'B', 'G', 'B', 'B'])
    test("eeeel", "eerie", ['G', 'G', 'B', 'B', 'Y'])
    test("chill", "legal", ['Y', 'B', 'B', 'B', 'G'])
    test("crane", "nacer", ['Y', 'Y', 'Y', 'Y', 'Y'])
    test("boost", "stoop", ['Y', 'Y', 'G', 'Y', 'B'])
    test("brand", "alarm", ['B', 'B', 'G', 'Y', 'B'])
    test("glass", "spasm", ['Y', 'B', 'G', 'G', 'B'])
    test("table", "bleat", ['Y', 'Y', 'Y', 'Y', 'Y'])
    test("tight", "blunt", ['B', 'B', 'B', 'B', 'G'])
    test("beers", "sweep", ['Y', 'B', 'G', 'Y', 'B'])
    test("mimic", "limit", ['B', 'G', 'G', 'G', 'B'])
    test("adobe", "kneel", ['B', 'B', 'Y', 'B', 'B'])

    print("All tests passed!")

run_tests()
