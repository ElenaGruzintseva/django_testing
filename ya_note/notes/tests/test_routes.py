from http import HTTPStatus

from .conftest import (
    TestBase, URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP,
    URL_NOTES_LIST, URL_NOTES_EDIT, URL_NOTES_DETAIL, URL_NOTES_DELETE
)


class TestRoutes(TestBase):

    def test_pages_availability_for_users(self):
        urls = (
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_NOTES_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_NOTES_EDIT, self.author_client, HTTPStatus.OK),
            (URL_NOTES_DELETE, self.author_client, HTTPStatus.OK),
            (URL_NOTES_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (URL_NOTES_EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (URL_NOTES_DELETE, self.reader_client, HTTPStatus.NOT_FOUND)
        )
        for url, client, status in urls:
            with self.subTest(url=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (URL_NOTES_LIST, f'{URL_LOGIN}?next={URL_NOTES_LIST}'),
            (URL_NOTES_DETAIL, f'{URL_LOGIN}?next={URL_NOTES_DETAIL}'),
            (URL_NOTES_EDIT, f'{URL_LOGIN}?next={URL_NOTES_EDIT}'),
            (URL_NOTES_DELETE, f'{URL_LOGIN}?next={URL_NOTES_DELETE}')
        )
        for url, redirect in urls:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect)
