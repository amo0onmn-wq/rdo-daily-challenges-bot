# rdo_client.py
import time
import logging
from typing import Dict, List, Any

import requests

from config import API_URL, CACHE_SECONDS

logger = logging.getLogger(__name__)

# كاش بسيط داخل الذاكرة
_CACHE_DATA = None
_CACHE_TIME = 0.0


def _normalize_role(raw_role: str) -> str:
    """تحويل اسم الدور من النص القادم من الـ API إلى مفتاح ثابت."""
    if not raw_role:
        return "general"

    r = str(raw_role).strip().lower()

    # احتمالات مختلفة
    if "bounty" in r:
        return "bounty"
    if "trader" in r:
        return "trader"
    if "collector" in r:
        return "collector"
    if "moonshiner" in r:
        return "moonshiner"
    if "naturalist" in r:
        return "naturalist"
    if "general" in r:
        return "general"

    # أي شيء ما تعرفنا عليه نرجعه كـ general
    return "general"


def _add_from_list(grouped: Dict[str, List[str]], items: Any, default_role: str = "general"):
    """إضافة مجموعة عناصر إلى القاموس حسب الـ role."""
    if not isinstance(items, list):
        return

    for item in items:
        if isinstance(item, dict):
            name = (
                item.get("name")
                or item.get("objective")
                or item.get("text")
                or ""
            )
            role = _normalize_role(
                item.get("role") or item.get("category") or default_role
            )
        else:
            name = str(item)
            role = default_role

        name = str(name).strip()
        if not name:
            continue

        grouped.setdefault(role, []).append(name)


def _parse_challenges(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    يحاول قراءة البيانات القادمة من الـ API وتقسيمها لأقسام:
    general, bounty, trader, collector, moonshiner, naturalist
    """
    grouped: Dict[str, List[str]] = {
        "general": [],
        "bounty": [],
        "trader": [],
        "collector": [],
        "moonshiner": [],
        "naturalist": [],
    }

    if not isinstance(data, dict):
        return grouped

    # محاولات مختلفة حسب احتمال تركيب JSON
    # 1) لو فيه مفتاح dailies
    dailies = data.get("dailies") or data.get("daily") or data.get("challenges")

    if isinstance(dailies, list):
        # سيناريو: قائمة كاملة فيها كل التحديات مع حقل role/category
        _add_from_list(grouped, dailies)
    elif isinstance(dailies, dict):
        # سيناريو: مفصول إلى general / bounty_hunter / trader ...
        for key, value in dailies.items():
            role = _normalize_role(key)
            _add_from_list(grouped, value, default_role=role)
    else:
        # fallback: نحاول نقرأ مباشرة من مفاتيح مشهورة
        for key in data.keys():
            value = data[key]
            role = _normalize_role(key)
            _add_from_list(grouped, value, default_role=role)

    return grouped


def fetch_challenges(force_refresh: bool = False) -> Dict[str, List[str]]:
    """
    يجلب التحديات من الـ API مع كاش بسيط.
    يرجع dict فيه قوائم لكل قسم:
    {
      "general": [...],
      "bounty": [...],
      "trader": [...],
      "collector": [...],
      "moonshiner": [...],
      "naturalist": [...]
    }
    """
    global _CACHE_DATA, _CACHE_TIME

    now = time.time()
    if not force_refresh and _CACHE_DATA is not None:
        if now - _CACHE_TIME < CACHE_SECONDS:
            return _CACHE_DATA

    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"Error fetching RDO challenges: {e}")
        # لو فيه كاش قديم نرجعه بدل لا شيء
        if _CACHE_DATA is not None:
            return _CACHE_DATA
        # وإلا نرجع هيكل فاضي
        return {
            "general": [],
            "bounty": [],
            "trader": [],
            "collector": [],
            "moonshiner": [],
            "naturalist": [],
        }

    grouped = _parse_challenges(data)

    _CACHE_DATA = grouped
    _CACHE_TIME = now

    return grouped
