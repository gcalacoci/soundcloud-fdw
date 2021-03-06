# Copyright (C) 2016 Giulio Calacoci
#
# This file is part of SoundcloudFDW.
#
# SoundcloudFDW is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SoundcloudFDW is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SoundcloudFDW.  If not, see <http://www.gnu.org/licenses/>.

from logging import ERROR, DEBUG

import soundcloud

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres


class SoundcloudForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
        """
        Init method for the Foreign Data Wrapper.

        Used to manage the apikey during the creation
        of the server on PostgreSQL

        :type options: Options passed during the creation of the FDW
        :type columns: the columns of the foreign table
        """
        super(SoundcloudForeignDataWrapper, self).__init__(options, columns)

        # The columns we'll be using (defaults to 'all'):
        self.columns = columns

        log_to_postgres('Soundcloud FDW Config options:  %s' % options, DEBUG)
        log_to_postgres('Soundcloud FDW Config columns:  %s' % columns, DEBUG)

        if 'apikey' not in options:
            log_to_postgres('Option apikey is required for '
                            'the Soundcloud FDW setup.', ERROR)
        self.apikey = options['apikey']

    def execute(self, quals, columns, **kwargs):
        """
        This method is invoked every time a SELECT is executed
        on the foreign table.

        Parses the quals argument searching for search criteria,
        contacts soundcloud using the official soundcloud python library
        and returns the search results inside the columns of the foreign table.

        Available columns are: title, url, search.

        :param list quals:a list of conditions which are used
          are used in the WHERE part of the select and can be used
          to restrict the number of the results
        :param list columns: the columns of the foreign table
        """
        if not quals:
            msg = 'specify a search term'
            log_to_postgres(level=ERROR, message=msg)
        # create a client object using the apikey
        client = soundcloud.Client(client_id=self.apikey)
        for qual in quals:
            # Manage quals, pass it as search therm if the field is 'search'
            if qual.field_name == "search" or qual.operator == "=":
                # Perform a simple search using the qual value
                # and the soundcloud client (limit to 10 results)
                tracks = client.get('/tracks', q=qual.value, limit=10)
                for track in tracks:
                    # Format the response line
                    line = {
                        'title': track.title,
                        'url': track.permalink_url,
                        'search': qual.value
                    }
                    yield line
