#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os


class test_state(test_basemodel):
    """ Defines test_state for BaseModel"""

    def __init__(self, *args, **kwargs):
        """ initialize test_states for BaseModel"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ test_name for state attr"""
        new = self.value()
        self.assertEqual(type(new.name), str )
