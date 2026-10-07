from app.db.models import Subscription, Vacancy


def matches_subscription(vacancy: Vacancy, subscription: Subscription) -> bool:
    """Match a vacancy by city and any keyword in its searchable fields."""
    if subscription.city and subscription.city.casefold() not in (vacancy.city or "").casefold():
        return False

    searchable = " ".join(
        part for part in [vacancy.title, vacancy.specialization, vacancy.introduction] if part
    ).casefold()
    return any(keyword.casefold() in searchable for keyword in subscription.keywords)
