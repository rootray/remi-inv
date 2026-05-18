from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.middleware import get_current_user
from backend.db.models import Rule, RuleAction, User
from backend.db.session import get_db

router = APIRouter(prefix="/rules", tags=["rules"])


class RuleCreate(BaseModel):
    name: str
    action: RuleAction
    threshold_amount: Optional[float] = None
    target_symbol: Optional[str] = None
    is_active: bool = True

    @model_validator(mode="after")
    def check_action_fields(self) -> "RuleCreate":
        if self.action == RuleAction.threshold and self.threshold_amount is None:
            raise ValueError("threshold_amount is required when action is 'threshold'")
        if self.action == RuleAction.target_symbol and not self.target_symbol:
            raise ValueError("target_symbol is required when action is 'target_symbol'")
        return self


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    action: Optional[RuleAction] = None
    threshold_amount: Optional[float] = None
    target_symbol: Optional[str] = None
    is_active: Optional[bool] = None


class RuleResponse(BaseModel):
    id: int
    name: str
    action: RuleAction
    threshold_amount: Optional[float]
    target_symbol: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}


@router.get("", response_model=list[RuleResponse])
async def list_rules(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Rule]:
    return list(await db.scalars(
        select(Rule).where(Rule.user_id == current_user.id).order_by(Rule.id)
    ))


@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    body: RuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Rule:
    rule = Rule(user_id=current_user.id, **body.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.patch("/{rule_id}", response_model=RuleResponse)
async def update_rule(
    rule_id: int,
    body: RuleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Rule:
    rule = await db.scalar(
        select(Rule).where(Rule.id == rule_id, Rule.user_id == current_user.id)
    )
    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    rule = await db.scalar(
        select(Rule).where(Rule.id == rule_id, Rule.user_id == current_user.id)
    )
    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    await db.delete(rule)
    await db.commit()
