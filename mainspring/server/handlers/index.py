"""Serves the single page app web ui."""

import json

from mainspring import settings
from mainspring import utils
from mainspring.server.handlers import base


class Handler(base.BaseHandler):
    """Index page request handler."""

    def get(self):
        """Serve up the single page app for scheduler dashboard."""

        meta_info = utils.get_all_available_jobs()
        self.render(settings.APP_INDEX_PAGE, jobs_meta_info=json.dumps(meta_info))
