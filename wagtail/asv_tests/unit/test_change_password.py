from unittest import mock
from unittest.mock import patch, MagicMock

from django.http.response import Http404

from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.admin.views.account import LoginView, change_password

class TestChangePassword(BaseTest):
    def setUp(self):
        super().setUp()
        
        # Arrange

        # Password reset POST request
        self.mock_request = MagicMock()
        self.mock_request.method = 'POST'
        self.mock_request.user = MagicMock()
        self.mock_request.user.has_usable_password = MagicMock(return_value=True)

        # Form validation
        self.mock_form = MagicMock()
        self.mock_form.is_valid = MagicMock(return_value=True)

    @mock.patch('wagtail.admin.views.account.password_management_enabled', autospec=True)
    @mock.patch('django.contrib.auth.forms.PasswordChangeForm', autospec=True)
    @mock.patch('django.contrib.auth.update_session_auth_hash', autospec=True)
    def test_change_password(self, mocked_pme, mocked_password_change_form, mocked_update_session):
        # Arrange
        mocked_pme.return_value = True
        mocked_password_change_form.return_value = self.mock_form

        # Act
        response = change_password(self.mock_request)
        
        # Assert
        assert mocked_update_session.called
        assert response.status_code == 302 and response.url == '/admin/account/'

    @mock.patch('wagtail.admin.views.account.password_management_enabled', autospec=True)
    @mock.patch('django.contrib.auth.forms.PasswordChangeForm', autospec=True)
    def test_get_password_form(self, mocked_pme, mocked_password_change_form):
        # Arrange
        self.mock_request.method = 'GET'
        self.mock_request.user.has_usable_password = MagicMock(return_value=True)
        mocked_pme.return_value = True
        mocked_password_change_form.return_value = self.mock_form

        with patch('django.template.loader.render_to_string') as mock_renderer:
            # Act
            response = change_password(self.mock_request)
        
        # Assert
        assert mocked_password_change_form.called and mock_renderer.called

    @mock.patch('wagtail.admin.views.account.password_management_enabled', autospec=True)
    def test_management_disabled(self, mocked_password_management):
        # Arrange
        mocked_password_management.return_value = False

        # Act and Assert
        with self.assertRaises(Http404) as context:
            # Expect 404 to be raised
            response = change_password(self.mock_request)
