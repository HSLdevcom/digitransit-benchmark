from locust import HttpLocust, TaskSet, task


class UIBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task
    def index(self):
        # CSS and SVG sprites are embedded in the HTML
        self.client.get("styleguidelines", name="ui")
        # JS code is in many bundles and would need parsing the HTML to get URLs
        # What's missing is not from UI server:
        # - one font (from Google)
        # - map tiles (from map server)
        # - stop information (from OTP server)


class User(HttpLocust):
    task_set = UIBehavior
    host = 'http://dev.digitransit.fi/'
