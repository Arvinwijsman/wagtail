from uuid import uuid4

from datetime import datetime, timezone
from unittest import mock
from unittest.mock import patch, MagicMock

from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ValidationError

from wagtail.core.models import BaseViewRestriction, Page, PageViewRestriction

from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.admin.forms.view_restrictions import BaseViewRestrictionForm
from wagtail.admin.forms.pages import WagtailAdminPageForm


class TestPageScheduling(BaseTest):
    def setUp(self):
        super().setUp()

        # Arrange
        with mock.patch.object(WagtailAdminPageForm, '__init__', return_value=None):
            self.form = WagtailAdminPageForm()  # pylint: disable=no-value-for-parameter
        
        self.form.parent_page = MagicMock()
    
    def test_valid_params(self):
        '''Tests a valid import of page scheduling params. '''
        # Arrange
        go_live_at = datetime(2020, 8, 15, 8, 15, 12, 0, timezone.utc)
        expire_at = datetime(2021, 8, 15, 8, 15, 12, 0, timezone.utc)

        # Act
        is_valid = self.form._validate_schedule_input(go_live_at, expire_at)

        # Assert
        assert is_valid

    def test_expire_in_past(self):
        '''Tests a past date given as expiry date. Expected to fail'''
        # Arrange
        go_live_at = datetime(2019, 8, 15, 8, 15, 12, 0, timezone.utc)
        expire_at = datetime(1999, 8, 15, 8, 15, 12, 0, timezone.utc)

        # Act
        with self.assertRaises(Exception) as context:
            is_valid = self.form._validate_schedule_input(go_live_at, expire_at)

            # assert
            assert not is_valid
