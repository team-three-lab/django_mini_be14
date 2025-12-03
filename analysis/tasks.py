from celery import shared_task
from django.utils import timezone
from .models import Analysis
from .services import compute_analysis_data


@shared_task
def run_analysis_task(analysis_id: int):
    analysis = Analysis.objects.get(pk=analysis_id)

    result = compute_analysis_data(analysis)

    image_url = ""  

    analysis.result_image = image_url
    analysis.last_run_at = timezone.now()
    analysis.save()

    return result  


@shared_task
def run_due_analyses_task():
    from django.utils import timezone

    now = timezone.now()
    today = now.date()

    analyses = Analysis.objects.filter(is_active=True)

    for analysis in analyses:
        if analysis.period == Analysis.AnalysisPeriod.DAILY:
            run_analysis_task.delay(analysis.id)

        elif analysis.period == Analysis.AnalysisPeriod.WEEKLY:
            if today.weekday() == 0: 
                run_analysis_task.delay(analysis.id)


        elif analysis.period == Analysis.AnalysisPeriod.MONTHLY:
            if today.day == 1:
                run_analysis_task.delay(analysis.id)


        elif analysis.period == Analysis.AnalysisPeriod.YEARLY:
            if today.month == 1 and today.day == 1:
                run_analysis_task.delay(analysis.id)