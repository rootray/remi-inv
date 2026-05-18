from decimal import Decimal

from backend.db.models import Rule, RuleAction


def evaluate(
    rules: list[Rule],
    source_symbol: str,
    dividend_amount: Decimal,
) -> tuple[str, bool]:
    """
    Returns (target_symbol, should_reinvest).
    Iterates active rules in order; first match wins.
    """
    for rule in rules:
        if not rule.is_active:
            continue
        if rule.action == RuleAction.reinvest_all:
            return source_symbol, True
        if rule.action == RuleAction.threshold:
            threshold = Decimal(str(rule.threshold_amount or 0))
            if dividend_amount >= threshold:
                return source_symbol, True
        if rule.action == RuleAction.target_symbol and rule.target_symbol:
            return rule.target_symbol, True
    return source_symbol, False
