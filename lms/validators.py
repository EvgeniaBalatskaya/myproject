from rest_framework.exceptions import ValidationError

def youtube_only_validator(value: str):
    if "youtube.com" not in value:
        raise ValidationError("Можно прикреплять только ссылки на youtube.com")
