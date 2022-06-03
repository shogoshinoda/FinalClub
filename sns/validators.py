from string import ascii_uppercase, ascii_lowercase, digits

from django.core.exceptions import ValidationError


def contain_any(target, condition_list):
    return any([i in target for i in condition_list])


class CustomValidator:
    message = "パスワードは(大小英字、数字）全てを組み合わせて設定してください。"

    def validate(self, password, user=None):
        if not all([contain_any(password, ascii_lowercase),
                    contain_any(password, ascii_uppercase),
                    contain_any(password, digits)]):
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message