from dndgame.entities import Entity


def test_get_modifier_positive():
    """A stat of 14 gives a +2 modifier: (14 - 10) // 2 == 2."""
    e = Entity("Test", {"STR": 14}, max_hp=10)
    assert e.get_modifier("STR") == 2


def test_get_modifier_negative():
    e = Entity("Test", {"STR": 8}, max_hp=10)
    assert e.get_modifier("STR") == -1


def test_is_alive_true_when_hp_positive():
    e = Entity("Test", {}, max_hp=5)
    assert e.is_alive is True


def test_is_alive_false_when_hp_zero():
    e = Entity("Test", {}, max_hp=5)
    e.hp = 0
    assert e.is_alive is False


def test_take_damage_normal_case():
    e = Entity("Test", {}, max_hp=10)
    lost = e.take_damage(4)
    assert lost == 4
    assert e.hp == 6


def test_take_damage_cannot_go_below_zero():
    """Overkill damage should floor HP at 0, not go negative."""
    e = Entity("Test", {}, max_hp=5)
    lost = e.take_damage(100)
    assert lost == 5
    assert e.hp == 0
    assert e.is_alive is False

def test_repr_shows_class_name_and_hp():
    e = Entity("Goblin", {"STR": 8}, max_hp=5)
    assert repr(e) == "Entity(name='Goblin', hp=5/5)"