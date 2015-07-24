#!/usr/bin/env python
# (C) British Crown Copyright 2010 - 2015, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""
Provides "diff-like" comparison of images.

Currently relies on matplotlib for image processing so limited to PNG format.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import os.path
import shutil
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mimg
import matplotlib.widgets as mwidget


def diff_viewer(expected_fname, result_fname, diff_fname):
    plt.figure(figsize=(16, 16))
    plt.suptitle(os.path.basename(expected_fname))
    ax = plt.subplot(221)
    ax.imshow(mimg.imread(expected_fname))
    ax = plt.subplot(222, sharex=ax, sharey=ax)
    ax.imshow(mimg.imread(result_fname))
    ax = plt.subplot(223, sharex=ax, sharey=ax)
    ax.imshow(mimg.imread(diff_fname))

    def accept(event):
        # removes the expected result, and move the most recent result in
        print('ACCEPTED NEW FILE: %s' % (os.path.basename(expected_fname), ))
        os.remove(expected_fname)
        shutil.copy2(result_fname, expected_fname)
        os.remove(diff_fname)
        plt.close()

    def reject(event):
        print('REJECTED: %s' % (os.path.basename(expected_fname), ))
        plt.close()

    ax_accept = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_reject = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = mwidget.Button(ax_accept, 'Accept change')
    bnext.on_clicked(accept)
    bprev = mwidget.Button(ax_reject, 'Reject')
    bprev.on_clicked(reject)

    plt.show()


def step_over_diffs():
    import iris.tests
    image_dir = os.path.join(os.path.dirname(iris.tests.__file__),
                             'results', 'visual_tests')
    diff_dir = os.path.join(os.path.dirname(iris.tests.__file__),
                            'result_image_comparison')

    for expected_fname in sorted(os.listdir(image_dir)):
        result_path = os.path.join(diff_dir, 'result-' + expected_fname)
        diff_path = result_path[:-4] + '-failed-diff.png'

        # if the test failed, there will be a diff file
        if os.path.exists(diff_path):
            expected_path = os.path.join(image_dir, expected_fname)
            diff_viewer(expected_path, result_path, diff_path)


if __name__ == '__main__':
    # Force iris.tests to use the ```tkagg``` backend by using the '-d'
    # command-line argument as idiff is an interactive tool that requires a
    # gui interface.
    sys.argv.append('-d')

    step_over_diffs()
