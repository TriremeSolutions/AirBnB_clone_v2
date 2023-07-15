#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
import json
import tests
import pep8
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestHBNBConsole(unittest.TestCase):
    """Unittest for the command line console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test

        Rename any existing json file temporarily.
        Reset FileStorage objects dictionary.
        Create an instance of the console.
        """
        try:
            os.rename("file.json", "tempfile")
        except IOError:
            pass
        cls.cli = HBNBCommand()

    @classmethod
    def teardown(cls):
        """
        Renames extant json file to normal
        Deletes the instance of the console
        """
        try:
            os.rename("tempfile", "file.json")
        except IOError:
            pass
        del cls.cli
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """test quit CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("quit")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """Test create CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd('create User email="a@mail.com" password="ftex"')
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

    def test_show(self):
        """Test show CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show invalid_nom")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show BaseModel rando-789")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all invalid_nom")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update invalid_nem")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update User 99999")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_aut_all(self):
        """Testing alternative all CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("invalid_nom.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_aut_count(self):
        """Test count CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("invalid_nom.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_aut_show(self):
        """Testing alternative show CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("invalid_nom.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("BaseModel.show(random-567)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Testing alternative destroy CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("randomtex.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """Testing alternative destroy CLI command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("invalid_nem.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
