from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Comment

BAD_WORDS = (
    'редиска',
    'негодяй',
)

WARNING = 'Не ругайтесь!'

FORM_DATA = {
    'text': 'Текст комментария.'
}

BAD_WORDS_DATA = {'text': f'Text, {BAD_WORDS[0]}, text'}


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        """Не позволяем ругаться в комментариях."""
        text = self.cleaned_data['text']
        lowered_text = text.lower()
        for word in BAD_WORDS:
            if word in lowered_text:
                raise ValidationError(WARNING)
        return text
