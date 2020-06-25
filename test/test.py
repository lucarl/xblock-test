"""An XBlock providing thumbs-up/thumbs-down voting."""

import logging

import pkg_resources
from six import text_type
from web_fragments.fragment import Fragment
from xblock.core import XBlock, XBlockAside
from xblock.fields import Boolean, Integer, Scope

log = logging.getLogger(__name__)


class TestXBlock(XBlock):
    """
    An XBlock with thumbs-up/thumbs-down voting.

    Vote totals are stored for all students to see.  Each student is recorded
    as has-voted or not.

    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    upvotes = Integer(help="Number of up votes", default=0,
                      scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0,
                        scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False,
                    scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # The student view composes and returns the fragment from static HTML, 
    # JavaScript, and CSS files. A web page displays the fragment to learners.
    def student_view(self, context=None):
        """
        The primary view of the TestXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/test.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/test.css"))
        frag.add_javascript(self.resource_string("static/js/src/test.js"))
        frag.initialize_js('TestXBlock')
        return frag

    # Handlers process input events from the XBlock JavaScript code.
    @XBlock.json_handler
    def vote(self, data, suffix=''):
        if data['voteType'] not in ('up', 'down'):
            log.error('error!')
            return

        if data['voteType'] == 'up':
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}

    # What you see in the workbench
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TestXBlock",
             """<test/>
             """),
            ("Multiple TestXBlock",
             """<vertical_demo>
                <test/>
                <test/>
                <test/>
                </vertical_demo>
             """),
        ]
