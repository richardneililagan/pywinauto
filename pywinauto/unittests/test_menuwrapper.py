# GUI Application automation and testing library
# Copyright (C) 2006-2018 Mark Mc Mahon and Contributors
# https://github.com/pywinauto/pywinauto/graphs/contributors
# http://pywinauto.readthedocs.io/en/latest/credits.html
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of pywinauto nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Tests for Menu"""

import sys
import os
import unittest
sys.path.append(".")
from pywinauto.application import Application
from pywinauto.sysinfo import is_x64_Python
from pywinauto.controls.menuwrapper import MenuItemNotEnabled
from pywinauto.timings import Timings


mfc_samples_folder = os.path.join(
   os.path.dirname(__file__), r"..\..\apps\MFC_samples")
if is_x64_Python():
    mfc_samples_folder = os.path.join(mfc_samples_folder, 'x64')


class MenuWrapperTests(unittest.TestCase):
    "Unit tests for the Menu and the MenuItem classes"

    def setUp(self):
        """Set some data and ensure the application is in the state we want"""
        Timings.defaults()

        self.app = Application()
        self.app.start("Notepad.exe")

        self.dlg = self.app.Notepad

    def tearDown(self):
        "Close the application after tests"
        self.app.kill_()

    def testInvalidHandle(self):
        "Test that an exception is raised with an invalid menu handle"
        # self.assertRaises(InvalidWindowHandle, HwndWrapper, -1)
        pass

    def testItemCount(self):
        self.assertEqual(5, self.dlg.Menu().ItemCount())

    def testItem(self):
        self.assertEqual(u'&File', self.dlg.Menu().Item(0).Text())
        self.assertEqual(u'&File', self.dlg.Menu().Item(u'File').Text())
        self.assertEqual(u'&File', self.dlg.Menu().Item(u'&File', exact=True).Text())

    def testItems(self):
        self.assertEqual([u'&File', u'&Edit', u'F&ormat', u'&View', u'&Help'],
                          [item.Text() for item in self.dlg.Menu().Items()])

    def testFriendlyClassName(self):
        self.assertEqual('MenuItem', self.dlg.Menu().Item(0).friendly_class_name())

    def testMenuItemNotEnabled(self):
        self.assertRaises(MenuItemNotEnabled, self.dlg.MenuSelect, 'Edit->Find Next')
        self.assertRaises(MenuItemNotEnabled, self.dlg.MenuItem('Edit->Find Next').Click)
        self.assertRaises(MenuItemNotEnabled, self.dlg.MenuItem('Edit->Find Next').click_input)

    def testGetProperties(self):
        self.assertEqual(
            {u'menu_items':
                [{u'index': 0, u'state': 0, u'item_type': 0, u'item_id': 64, u'text': u'View &Help'},
                 {u'index': 1, u'state': 3, u'item_type': 2048, u'item_id': 0, u'text': u''},
                 {u'index': 2, u'state': 0, u'item_type': 0, u'item_id': 65, u'text': u'&About Notepad'}]},
            self.dlg.Menu().GetMenuPath('Help')[0].SubMenu().GetProperties())

    def testGetMenuPath(self):
        # print('id = ' + str(self.dlg.Menu().GetMenuPath('Help->#3')[0].id()))
        self.assertEqual(u'&About Notepad', self.dlg.Menu().GetMenuPath(' Help -> #2 ')[-1].Text())
        self.assertEqual(u'&About Notepad', self.dlg.Menu().GetMenuPath('Help->$65')[-1].Text())
        self.assertEqual(u'&About Notepad',
                          self.dlg.Menu().GetMenuPath('&Help->&About Notepad', exact=True)[-1].Text())
        self.assertRaises(IndexError, self.dlg.Menu().GetMenuPath, '&Help->About what?', exact=True)

    def test__repr__(self):
        print(self.dlg.Menu())
        print(self.dlg.Menu().GetMenuPath('&Help->&About Notepad', exact=True)[-1])

    def testClick(self):
        self.dlg.Menu().GetMenuPath('&Help->&About Notepad')[-1].Click()
        About = self.app.Window_(title='About Notepad')
        About.Wait('ready')
        About.OK.Click()
        About.WaitNot('visible')

    def testClickInput(self):
        self.dlg.Menu().GetMenuPath('&Help->&About Notepad')[-1].click_input()
        About = self.app.Window_(title='About Notepad')
        About.Wait('ready')
        About.OK.Click()
        About.WaitNot('visible')


class OwnerDrawnMenuTests(unittest.TestCase):

    """Unit tests for the OWNERDRAW menu items"""

    def setUp(self):
        """Set some data and ensure the application is in the state we want"""
        Timings.defaults()

        self.app = Application().Start(os.path.join(mfc_samples_folder, u"BCDialogMenu.exe"))
        self.dlg = self.app.BCDialogMenu
        self.app.wait_cpu_usage_lower(threshold=1.5, timeout=30, usage_interval=1)
        self.dlg.wait('ready')

    def tearDown(self):
        """Close the application after tests"""
        self.app.kill_()

    def testCorrectText(self):
        menu = self.dlg.Menu()
        self.assertEqual(u'&New', menu.GetMenuPath('&File->#0')[-1].Text()[:4])
        self.assertEqual(u'&Open...', menu.GetMenuPath('&File->#1')[-1].Text()[:8])


if __name__ == "__main__":
    unittest.main()
