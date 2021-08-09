from manset.manset_gui import MansetGUI


def test_gui():
    gui = MansetGUI()
    gui.plot()
    assert gui.destroy_gui() is True
