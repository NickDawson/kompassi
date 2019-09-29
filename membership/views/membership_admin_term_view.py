from ..helpers import membership_admin_required
from django.views.decorators.http import require_http_methods


@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_term_view(request, vars, organization, term_id=None):
    raise NotImplementedError()
