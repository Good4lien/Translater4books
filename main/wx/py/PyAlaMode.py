#!/usr/bin/env python
"""PyAlaMode is a programmer's editor."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import wx
from wx import py

import os
import sys

class App(wx.App):
    """PyAlaMode standalone application."""

    def __init__(self, filename=None):
        self.filename = filename
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        self.frame = py.editor.EditorNotebookFrame(filename=self.filename)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main(filename=None):
    if not filename and len(sys.argv) > 1:
        filename = sys.argv[1]
    if filename:
        filename = os.path.realpath(filename)
    app = App(filename)
    app.MainLoop()

if __name__ == '__main__':
    main()
