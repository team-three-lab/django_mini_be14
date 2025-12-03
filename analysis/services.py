from collections import defaultdict
from transactions.models import Transaction


def compute_analysis_data(analysis):
    qs = Transaction.objects.filter(
        account=analysis.account,
        is_deposit=analysis.is_income,
        transacted_at__range=(analysis.start_date, analysis.end_date),
    ).order_by("transacted_at")

    total_amount = sum(t.amount for t in qs)

    daily_chart = defaultdict(int)
    type_chart = defaultdict(int)
    description_chart = defaultdict(int)

    for t in qs:
        day = t.transacted_at.date().isoformat()
        daily_chart[day] += t.amount

        ttype = t.transaction_type
        type_chart[ttype] += t.amount

        desc = t.description or "기타"
        description_chart[desc] += t.amount

    data = {
        "analysis": {
            "id": analysis.id,
            "account": analysis.account.id,
            "is_income": analysis.is_income,
            "period": analysis.period,
            "start_date": analysis.start_date,
            "end_date": analysis.end_date,
            "description": analysis.description,
        },
        "summary": {
            "total_amount": total_amount,
            "transactions_count": qs.count(),
        },
        "daily_chart": dict(daily_chart),
        "type_chart": dict(type_chart),
        "description_chart": dict(description_chart),
    }

    return data
