from django.urls import reverse


SLUG = 'Zametka-1'
URL_HOME = reverse('notes:home')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_NOTES_LIST = reverse('notes:list')
URL_NOTES_ADD = reverse('notes:add')
URL_NOTES_SUCCESS = reverse('notes:success')
URL_NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
URL_NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_NOTES_DELETE = reverse('notes:delete', args=(SLUG,))
