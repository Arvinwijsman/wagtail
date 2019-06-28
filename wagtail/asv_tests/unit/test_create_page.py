from unittest import mock
from unittest.mock import patch, MagicMock

from wagtail.asv_tests.unit.base_test import BaseTest
from wagtail.admin.views.pages import create, _create_page

from time import time

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponse, JsonResponse
from django.http.request import QueryDict
# from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.http import is_safe_url, urlquote
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.vary import vary_on_headers
from django.views.generic import View

from wagtail.admin import messages, signals
from wagtail.admin.action_menu import PageActionMenu
from wagtail.admin.forms.pages import CopyForm
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.navigation import get_explorable_root_page
from wagtail.admin.utils import send_notification, user_has_any_page_permission, user_passes_test
from wagtail.core import hooks
from wagtail.core.models import Page, PageRevision, UserPagePermissionsProxy
from wagtail.search.query import MATCH_ALL

class TestCreatePage(BaseTest):
    def setUp(self):
        super().setUp()

        # Arrange mock page setup
        self.request = MagicMock()
        self.parent_page_id = 99999
        self.mock_page = {
            'title':'Public page',
            'content':'hello',
            'live':True,
        }
        self.queryset = MagicMock()
        self.queryset.model = 'page'

        self.mock_form = MagicMock()
        self.mock_form.is_valid = MagicMock(return_value=True)
        self.mock_form.save = MagicMock(return_value=self.mock_page)

        self.request.method = 'POST'
        self.request.POST = {
            'action-publish': True,
            'action-submit': True
        }
        self.form_class = MagicMock(return_value=self.mock_form)
        self.parent_page_perms = MagicMock()
        self.parent_page_perms.can_publish_subpage = MagicMock(return_value=True)
        self.parent_page = MagicMock()
        self.parent_page.add_child = MagicMock()
        self.revision = MagicMock(return_value=False)
        self.revision.publish = MagicMock()
    
    @mock.patch('django.shortcuts._get_queryset')
    @mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_by_natural_key')
    @mock.patch('wagtail.admin.views.pages._notify_user')
    def test_submit_page(self, mock_query, mock_get_key, mock_notify):
        # Arrange
        with mock.patch.object(Page, '__init__', return_value=None):
            self.page = Page()  # pylint: disable=no-value-for-parameter    
            self.page.save_revision = MagicMock(return_value=self.revision)

        self.mock_form.save = MagicMock(return_value=self.page)
        redirection_url = 'wagtailadmin/pages/created.html'

        # Act
        response = _create_page(
            request=self.request, 
            form_class=self.form_class, 
            parent_page_perms=self.parent_page_perms,
            parent_page=self.parent_page,
            next_url=redirection_url,
            content_type='type',
            page_class='class',
            page=self.page
        )
        
        # Assert
        assert self.parent_page.add_child.called
        assert self.revision.publish.called
        assert response.status_code == 302 and response.url == redirection_url
