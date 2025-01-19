import pytest
from PyQt6.QtCore import Qt, QSize
from unittest import mock
from ui import MyTestApp

@pytest.fixture
def app():
    app = MyTestApp()
    app.show()
    return app

def test_window_properties(app):
    assert app.windowTitle() == "Operating System Info"
    assert app.size().width() == 500
    assert app.size().height() == 600
    
def test_button_click(app, qtbot):
    button = app.layout.itemAt(1).widget()
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    text_view_content = app.text_view.toPlainText()
    assert "Network" in text_view_content

def test_error_handling(app, qtbot, monkeypatch):
    def mock_get_system_info():
        raise Exception("Error fetching system info")
    monkeypatch.setattr("modules.system_info.get_system_info", mock_get_system_info)
    button = app.layout.itemAt(2).widget()
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    text_view_content = app.text_view.toPlainText()
    assert "Error fetching system info" in text_view_content

def test_button_positioning(app):
    button = app.layout.itemAt(1).widget()
    assert button.pos().y() > app.text_view.pos().y()

def test_text_font_size(app):
    font = app.text_view.font()
    assert font.pointSize() == 16

def test_button_styling(app):
    button = app.layout.itemAt(1).widget()
    button_style = button.styleSheet()
    assert "background-color: #136095;" in button_style
    assert "font-size: 16px;" in button_style

def test_responsiveness(app, qtbot):
    initial_size = app.size()
    new_size = initial_size + QSize(100, 100)
    app.resize(new_size)
    qtbot.wait(500)
    assert app.size() != initial_size
    text_view_size = app.text_view.size()
    assert text_view_size.width() <= new_size.width()

def test_keyboard_navigation(app, qtbot):
    button = app.layout.itemAt(1).widget()
    button.setFocus()
    qtbot.keyClick(button, Qt.Key_Tab)
    next_button = app.layout.itemAt(2).widget()
    assert next_button.hasFocus()

def test_button_color_contrast(app):
    button = app.layout.itemAt(1).widget()
    button_style = button.styleSheet()
    assert "color: #fafafa;" in button_style
    assert "background-color: #136095;" in button_style

def test_button_visibility(app):
    buttons = [app.layout.itemAt(i).widget() for i in range(app.layout.count()) if isinstance(app.layout.itemAt(i).widget(), QtWidgets.QPushButton)]
    for button in buttons:
        assert button.isVisible()

def test_ui_text_content(app):
    text_view_content = app.text_view.toPlainText()
    assert text_view_content == ""

def test_ui_background_color(app):
    window_style = app.styleSheet()
    assert "background-color: #f0f0f0;" in window_style

def test_button_alignment(app):
    first_button = app.layout.itemAt(1).widget()
    second_button = app.layout.itemAt(2).widget()
    assert first_button.pos().x() == second_button.pos().x()

def test_window_title(app):
    assert app.windowTitle() == "Operating System Info"

def test_button_size(app):
    button = app.layout.itemAt(1).widget()
    assert button.size() == QSize(200, 50)