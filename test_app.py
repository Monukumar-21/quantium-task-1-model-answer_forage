import pytest
from dash.testing.application_runners import import_app

# Import your Dash app (assuming it's saved as app.py)
@pytest.fixture
def dash_app():
    app = import_app("app")  # "app" is the filename without .py
    return app


def test_header_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods Sales Visualiser"


def test_visualisation_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None


def test_region_picker_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None