import unittest

from app import create_app
from app.state import state


HD_PROGRAMS_LIST = ["candle", "demo", "forest_fire", "game_of_life", "rainbow", 
    "stars", "trig"]
ORIGINAL_PROGRAMS_LIST = ["ascii_text", "cheertree", "cross", "demo", "dna", 
    "game_of_life", "matrix", "psychedelia", "rain", "rainbow", 
    "random_blinky", "random_sparkles", "simple", "snow", "trig"]


class TestAPI(unittest.TestCase):
    
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def tearDown(self):
        state.stop_program()

    def test_start_all_hd(self):
        state.set_model(is_hd=True)
        for program in HD_PROGRAMS_LIST:
            with self.subTest(program=program):
                r = self.app.put("/api/program/" + program)
                self.assertEqual(r.status_code, 200)

    def test_start_all_original(self):
        state.set_model(is_hd=False)
        for program in ORIGINAL_PROGRAMS_LIST:
            with self.subTest(program=program):
                r = self.app.put("/api/program/" + program)
                self.assertEqual(r.status_code, 200)

    def test_start_not_found(self):
        r = self.app.put("/api/program/does_not_exist")
        self.assertEqual(r.status_code, 404)

    def test_start_with_good_params(self):
        r = self.app.put("/api/program/demo?brightness=0.5&rotation=0")
        self.assertEqual(r.status_code, 200)

    def test_start_with_bad_brightness(self):
        r = self.app.put("/api/program/demo?brightness=1.1")
        self.assertEqual(r.status_code, 400)

    def test_start_with_bad_rotation(self):
        r = self.app.put("/api/program/demo?rotation=91")
        self.assertEqual(r.status_code, 400)

    def test_stop_program(self):
        r = self.app.delete("/api/program")
        self.assertEqual(r.status_code, 200)