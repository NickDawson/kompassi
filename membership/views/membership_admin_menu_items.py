from core.admin_menus import AdminMenuItem
from core.utils import url


def membership_admin_menu_items(request, organization):
    members_url = url('membership_admin_members_view', organization.slug)
    members_active = request.path.startswith(members_url)
    members_text = 'Jäsenrekisteri'

    term_url = url('membership_admin_current_term_view', organization.slug)
    term_active = request.path.startswith(term_url)
    term_text = 'Toimikauden tiedot'
    term_notifications = 1 if organization.membership_organization_meta.get_current_term() is None else 0

    return [
        AdminMenuItem(is_active=members_active, href=members_url, text=members_text),
        AdminMenuItem(is_active=term_active, href=term_url, text=term_text, notifications=term_notifications),
    ]
