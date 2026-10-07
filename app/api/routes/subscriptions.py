from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Subscription
from app.db.session import get_db
from app.schemas.subscriptions import SubscriptionCreate, SubscriptionDeleted, SubscriptionRead

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)) -> Subscription:
    subscription = Subscription(**payload.model_dump())
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@router.get("/{subscription_id}", response_model=SubscriptionRead)
def get_subscription(subscription_id: UUID, db: Session = Depends(get_db)) -> Subscription:
    subscription = db.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.delete("/{subscription_id}", response_model=SubscriptionDeleted)
def deactivate_subscription(subscription_id: UUID, db: Session = Depends(get_db)) -> Subscription:
    subscription = db.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.is_active = False
    db.commit()
    return subscription
