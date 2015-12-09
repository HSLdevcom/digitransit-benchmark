from locust import HttpLocust, TaskSet, task

class FrontpageBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task(2)
    def index(self):
        # CSS and SVG sprites are embedded in the HTML
        self.client.get("/", name="frontpage")
        # All JS code is in one file
        self.client.get("/js/bundle.js", name="frontpage")
        # What's missing is not from UI server:
        # - one font (from Google)
        # - map tiles (from map server)
        # - stop information (from OTP server)


class FrontpageUser(HttpLocust):
    task_set = FrontpageBehavior
    host = 'http://dev.digitransit.fi/'
