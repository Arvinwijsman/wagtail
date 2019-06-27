from uuid import uuid4

import unittest
from unittest import mock
from unittest.mock import MagicMock

from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ValidationError

from wagtail.core.models import BaseViewRestriction

from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.admin.forms.view_restrictions import BaseViewRestrictionForm


class TestViewRestrictions(BaseTest):
    def setUp(self):
        super().setUp()
        with mock.patch.object(BaseViewRestrictionForm, '__init__', return_value=None):
            self.form = BaseViewRestrictionForm()  # pylint: disable=no-value-for-parameter
        self.form.fields = MagicMock()
        self.form.fields['groups'].widget = MagicMock()
        self.form.fields['groups'].queryset = MagicMock()
    
class TestRequiredFields(TestViewRestrictions):
    def setUp(self):
        super().setUp()

        # Mock inputs
        self.valid_data_password = {
            'password': 'unh4ackable',
            'restriction_type': BaseViewRestriction.PASSWORD,
        }
        self.valid_data_groups = {
            'restriction_type': BaseViewRestriction.GROUPS,
            'groups': 'group1'
        }
    
    def test_password_field_valid(self):
        '''Tests the happy flow of password form validation '''
        # Setup
        self.form.cleaned_data = self.valid_data_password
        expected = 'unh4ackable'

        # Run
        result = self.form.clean_password()

        # Assert
        assert result == expected

    def test_password_field_invalid(self):
        '''Tests exception thrown for invalid input. '''
        # Setup
        self.form.cleaned_data = self.valid_data_password
        self.form.cleaned_data.pop('password')

        # Run
        with self.assertRaises(ValidationError) as context:
            self.form.clean_password()

            # Assert
            assert context.message == "This field is required."

    def test_group_field_valid(self):
        '''Tests the happy flow of group form validation '''
        # Setup
        self.form.cleaned_data = self.valid_data_groups
        expected = 'group1'

        # Run
        result = self.form.clean_groups()

        # Assert
        assert result == expected

    def test_group_field_invalid(self):
        '''Tests exception thrown for invalid input. '''
        # Setup
        self.form.cleaned_data = self.valid_data_groups
        self.form.cleaned_data.pop('groups')

        # Run and assert
        with self.assertRaises(ValidationError) as context:
            self.form.clean_groups()
    