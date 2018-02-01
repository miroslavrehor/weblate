# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
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

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from weblate.addons.base import BaseAddon
from weblate.addons.events import EVENT_PRE_COMMIT
from weblate.trans.exporters import MoExporter


class GenerateMoAddon(BaseAddon):
    events = (EVENT_PRE_COMMIT,)
    name = 'weblate.gettext.mo'
    compat = {
        'file_format': frozenset((
            'auto', 'po', 'po-unwrapped', 'po-mono', 'po-mono-unwrapped'
        )),
    }
    verbose = _('Generate mo files')
    description = _(
        'Automatically generates mo file for every changed po file.'
    )

    def pre_commit(self, translation):
        exporter = MoExporter(translation=translation)
        exporter.add_units(translation)
        output = translation.get_filename()[:-2] + 'mo'
        with open(output, 'wb') as handle:
            handle.write(exporter.serialize())
        translation.addon_commit_files.append(output)

    @classmethod
    def is_compatible(cls, component):
        if not component.filemask.endswith('.po'):
            return False
        return super(GenerateMoAddon, cls).is_compatible(component)