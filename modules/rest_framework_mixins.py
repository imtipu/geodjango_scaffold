class RequestMixin(object):
    def _request(self):
        return self.context['request']