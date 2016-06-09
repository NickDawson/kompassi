from django.conf.urls import include, url
from django.shortcuts import redirect

from .views import (
    badges_admin_badges_view,
    badges_admin_batches_view,
    badges_admin_create_view,
    badges_admin_dashboard_view,
    badges_admin_export_view,
    badges_admin_onboarding_view,
)


urlpatterns = [
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/?$',
        badges_admin_dashboard_view,
        name='badges_admin_dashboard_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/badges/?$',
        badges_admin_badges_view,
        name='badges_admin_badges_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/badges/new/?$',
        badges_admin_create_view,
        name='badges_admin_create_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/badges/(?P<personnel_class_slug>[a-z0-9-]+)/?$',
        badges_admin_badges_view,
        name='badges_admin_filtered_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/badges/(?P<personnel_class_slug>[a-z0-9-]+)/new/?$',
        badges_admin_create_view,
        name='badges_admin_create_with_template_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/batches/?$',
        badges_admin_batches_view,
        name='badges_admin_batches_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/batches/(?P<batch_id>\d+)\.(?P<format>csv|tsv|xlsx)?$',
        badges_admin_export_view,
        name='badges_admin_export_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/onboarding/?$',
        badges_admin_onboarding_view,
        name='badges_admin_onboarding_view',
    ),

]
