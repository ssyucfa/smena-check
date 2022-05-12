import io

from celery import shared_task
import pdfkit
from django.core.files import File


from checks.models import Check, CheckStatus
from .service import get_rendered_template


@shared_task
def create_pdf_for_checks(checks_id: list[int]) -> None:
    checks = Check.objects.filter(pk__in=checks_id)
    for check in checks:
        check_str = get_rendered_template(check)
        pdf = File(io.BytesIO(pdfkit.from_string(check_str)), f'check_{check.id}-{check.type}.pdf')
        check.pdf = pdf
        check.status = CheckStatus.RENDERED
        check.save()
