from unittest import mock
from unittest.mock import patch, MagicMock

from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.users.views.users import create

class TestUserCreation(BaseTest):
    def setUp(self):
        super().setUp()
        self.request = MagicMock()
        self.mock_form = MagicMock()

    
    @mock.patch('wagtail.users.views.users.get_user_creation_form')
    def test_get_user_creation_form(self, mock_get_user_creation_form):
        # Arrange
        self.request.method = 'GET'
        mock_get_user_creation_form.return_value = self.mock_form

        # Act
        with patch('django.template.loader.render_to_string') as mock_renderer:
            response = create(self.request)
        
        # Assert
        assert mock_get_user_creation_form.called
        assert response.status_code == 200

    @mock.patch('wagtail.users.views.users.get_user_creation_form')
    @mock.patch('wagtail.admin.messages.success')
    def test_create_user_success(self, mock_get_user_creation_form, mock_success_msg):
        # Arrange
        self.mock_form.is_valid = MagicMock(return_value=True)
        self.mock_form.save = MagicMock(return_value="Austin Powers")
        self.request.method = 'POST'
        self.mock_form.return_value = self.mock_form
        mock_get_user_creation_form.return_value = self.mock_form

        # Act
        response = create(self.request)
        
        # Assert
        expected_url = '/admin/users/'
        assert mock_get_user_creation_form.called
        assert mock_success_msg.called
        assert response.status_code == 302 and response.url == expected_url
    
    @mock.patch('wagtail.users.views.users.get_user_creation_form')
    @mock.patch('wagtail.admin.messages.error')
    def test_create_user_invalid_form(self, mock_get_user_creation_form, mock_error_msg):
        # Arrange
        self.request.method = 'POST'
        self.mock_form.is_valid = MagicMock(return_value=False) # causes the submittion to fail
        self.mock_form.return_value = self.mock_form
        mock_get_user_creation_form.return_value = self.mock_form

        # Act
        with patch('django.template.loader.render_to_string') as mock_renderer:
            create(self.request)
        
        # Assert
        assert mock_error_msg.called
        
