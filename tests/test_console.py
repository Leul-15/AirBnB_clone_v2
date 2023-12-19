#!/usr/bin/python3
""" """
import os
import models
import pep8
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """Unittests HBNBCommand
    """

    @classmethod
    def setUpClass(cls):
        """Temporarily Rename file.json"""
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        cls.HBNBC = HBNBCommand()
    
    @classmethod
    def tearDownClass(cls):
        """Restore original file.json
        """
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        del cls.HBNBC
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()
    
    def setUp(self):
        """Reset FileStorage
        """
        FileStorage._FileStorage__objects = {}
    
    def tearDown(self):
        """Delete created file.json
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
    
    def test_pep8(self):
        """Test pep8
        """
        st = pep8.StyleGuide(quiet=True)
        result = st.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors")
    
    def test_docstring(self):
        """Test docstring
        """
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
    
    def test_emptyline(self):
        """Test empty line
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNBC.onecmd("\n")
            self.assertEqual("", f.getvalue())
    
    def test_quit(self):
        """Test quit
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNBC.onecmd("quit")
            self.assertEqual("", f.getvalue())
    
    def test_EOF(self):
        """Test EOF
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.HBNBC.onecmd("EOF"))
