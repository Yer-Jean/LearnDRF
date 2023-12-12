from rest_framework.serializers import ValidationError


class VideoURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        temp_value = dict(value).get(self.field)
        if temp_value:
            if temp_value.find('youtube.') == -1 and temp_value.find('youtu.be') == -1 and temp_value.find('yt.be') == -1:
                raise ValidationError('The video is not posted on YouTube')
