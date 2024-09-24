#!@PYTHON@

# Copyright 2024 Robson Cardoso dos Santos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext
import locale
import os
import signal
import sys

VERSION = '@VERSION@'
pkgdatadir = '@pkgdatadir@'
localedir = '@localedir@'

sys.path.insert(1, pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)
locale.bindtextdomain('codarium', localedir)
locale.textdomain('codarium')
gettext.install('codarium', localedir)

if __name__ == '__main__':
    import gi
    from gi.repository import Gio
    resource = Gio.Resource.load(os.path.join(pkgdatadir, 'codarium.gresource'))
    resource._register()

    # from codarium import main
    from src.main import main
    sys.exit(main.main(VERSION))
