from collections import OrderedDict
from logging import ERROR

import soundcloud

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres

import config as c


class SoundcloudForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
        super(SoundcloudForeignDataWrapper, self).__init__(options, columns)
        self.columns = columns

    def execute(self, quals, columns):
        if not quals:
            msg = 'specify a search'
            log_to_postgres(level=ERROR, message=msg)
        # create a client object using the apikey
        client = soundcloud.Client(client_id=c.apikey)
        for qual in quals:
            # Manage quals, pass it as search therm if the field is 'search'
            if qual.field_name == "search" or qual.operator == "=":
                # Perform a simple search using the qual value
                # and the soundcloud client
                tracks = client.get('/tracks', q=qual.value)
                for track in tracks:
                    # Format the response line
                    line = {
                        'title': track.title,
                        'url': track.permalink_url,
                        'search': qual.value
                    }
                    # log_to_postgres('%s' % str(line))
                    yield line
