from uuid import uuid4

from datetime import datetime, timezone
from unittest import mock
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import Group
from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.users.forms import GroupForm

class TestCreateUserGroup(BaseTest):
    def setUp(self):
        super().setUp()

        # Arrange
        with mock.patch.object(GroupForm, '__init__', return_value=None):
            self.form = GroupForm()  # pylint: disable=no-value-for-parameter
        
        self.form.registered_permissions = MagicMock()
        self.form.instance = MagicMock()
        self.fields = {}
        self.fields['permissions'] = MagicMock()
        self.fields['permissions'].queryset = MagicMock()
    

    def test_duplicate_name_exception(self):
        # Arrange
        self.form.cleaned_data = {
            'name': 'groupname'
        }
        self.form.instance.pk = MagicMock()
        Group._default_manager.exclude = MagicMock(side_effect=Exception)

        # Act
        with self.assertRaises(Exception) as context:
            result = self.form.clean_name()

            # Assert
            assert result == 'groupname'
    
    @mock.patch('django.forms.forms.BaseForm')
    def test_save_group(self, mock_form):
        # Arrange
        self.form.save = MagicMock(return_value='group1')
        self.form.instance.permissions = MagicMock()
        self.form.instance.permissions.exclude = MagicMock(return_value=True)

        expected_group = 'group1'

        # Act
        result_group = self.form.save()
        
        # Assert
        assert result_group == expected_group

    def test_group_saving_exception(self):
        # Arrange
        self.form.instance = MagicMock()
        self.form.instance.permissions = MagicMock()
        self.form.instance.permissions.exclude = MagicMock(
            side_effect=ValueError
        )

        # Act and Assert
        with self.assertRaises(AttributeError) as context:
            self.form.save()

