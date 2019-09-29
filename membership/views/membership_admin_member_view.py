from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from api.utils import api_login_required, handle_api_errors
from core.admin_menus import AdminMenuItem
from core.csv_export import CSV_EXPORT_FORMATS, csv_response
from core.models import Organization
from core.sort_and_filter import Filter
from core.tabs import Tab
from core.utils import initialize_form, url
from event_log.utils import emit
from tickets.utils import format_price

from ..forms import MemberForm, MembershipFeePaymentForm, MembershipForm
from ..helpers import membership_admin_required
from ..models import STATE_CHOICES, Membership, MembershipFeeNonPayment, MembershipFeePayment


@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_member_view(request, vars, organization, person_id):
    membership = get_object_or_404(Membership, organization=organization, person=int(person_id))
    read_only = membership.person.user is not None
    member_form = initialize_form(MemberForm, request, instance=membership.person, readonly=read_only, prefix='member')
    membership_form = initialize_form(MembershipForm, request, instance=membership, prefix='membership')

    forms = [membership_form] if read_only else [membership_form, member_form]

    membership_fee_payments = MembershipFeePayment.objects.filter(
        term__organization=organization, member=membership
    ).order_by('term__end_date')
    current_term = membership.meta.get_current_term()

    if current_term and current_term.membership_fee_cents and not MembershipFeePayment.objects.filter(term=current_term, member=membership).exists():
        current_term_nonpayment = MembershipFeeNonPayment(term=current_term, amount_cents=current_term.membership_fee_cents)
        membership_fee_payments = list(membership_fee_payments) + [current_term_nonpayment, ]
        membership_fee_payment_form = initialize_form(MembershipFeePaymentForm, request, current_term=current_term)
    else:
        messages.warning(request, 'Nykyisen toimikauden tiedot puuttuvat. Syötä tiedot Toimikauden tiedot -näkymässä.')
        membership_fee_payment_form = None

    if request.method == 'POST':
        action = request.POST['action']

        if action in ['save-edit', 'save-return']:
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                membership.apply_state()

                messages.success(request, 'Jäsenen tiedot tallennettiin.')

                if action == 'save-return':
                    return redirect('membership_admin_members_view', organization.slug)

            else:
                messages.error(request, 'Tarkista lomakkeen tiedot.')
        elif action == 'mark-paid':
            payment = membership_fee_payment_form.save(commit=False)
            payment.member = membership
            payment.save()

            messages.success(request, 'Jäsenmaksu merkattiin maksetuksi.')
            return redirect('membership_admin_member_view', organization.slug, membership.person.id)
        else:
            raise NotImplementedError(action)

    previous_membership, next_membership = membership.get_previous_and_next()

    tabs = [
        Tab('membership-admin-person-tab', 'Jäsenen tiedot', active=True),
        Tab('membership-admin-state-tab', 'Jäsenyyden tila'),
        # Tab('membership-admin-events-tab', 'Jäsenyyteen liittyvät tapahtumat'),
        Tab('membership-admin-payments-tab', 'Jäsenmaksut'),
    ]

    vars.update(
        current_term=current_term,
        member_form=member_form,
        member=membership.person,
        membership_fee_payment_form=membership_fee_payment_form,
        membership_fee_payments=membership_fee_payments,
        membership_form=membership_form,
        membership=membership,
        next_membership=next_membership,
        previous_membership=previous_membership,
        read_only=read_only,
        tabs=tabs,
    )

    membership.person.log_view(request)

    return render(request, 'membership_admin_member_view.pug', vars)
