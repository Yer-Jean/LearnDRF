from rest_framework.serializers import ValidationError


class VideoURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value.__dict__)
        temp_value = dict(value).get(self.field)
        print(temp_value)
        tmp = temp_value.find('youtube.')
        if temp_value.find('youtube.') == -1 and temp_value.find('youtu.be') == -1 and temp_value.find('yt.be') == -1:
            raise ValidationError('The video is not posted on YouTube')
