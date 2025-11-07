# formatting.py
from typing import List, Dict

from config import ARABIC_ROLE_TITLES


def format_single_group(role_key: str, items: List[str]) -> str:
    """صياغة مجموعة واحدة (مثلاً تحديات التاجر) كنص جاهز للإرسال."""
    title = ARABIC_ROLE_TITLES.get(role_key, role_key)

    if not items:
        return f"⭐️ *{title}*\nلا توجد تحديات متاحة حاليًا لهذا الدور."

    lines = [f"⭐️ *{title}*"]
    lines.append("")  # سطر فاضي

    # نخلي نص التحدي الأصلي كما هو، ونضيف صيغة أمر بالعربي
    for i, text in enumerate(items, start=1):
        # مثال: "1. أنجز التحدي التالي: 5 Blackcurrants picked"
        lines.append(f"{i}. أنجز التحدي التالي:\n   {text}")

    return "\n".join(lines)


def format_full_all(groups: Dict[str, List[str]]) -> str:
    """صياغة رسالة كاملة فيها كل الأقسام (عام + كل الأدوار)."""
    order = ["general", "bounty", "trader", "collector", "moonshiner", "naturalist"]
    parts: List[str] = []

    header = (
        "🔥 *التحديات اليومية لليوم في Red Dead Online*\n\n"
        "كل سطر فيه صيغة أمر بالعربي مع نص التحدي الأصلي بالإنجليزي، "
        "حتى تبقى أسماء الحيوانات والنباتات كما هي 🌿🦬\n\n"
    )
    parts.append(header)

    for key in order:
        section = format_single_group(key, groups.get(key, []))
        parts.append(section)
        parts.append("")  # سطر فاصل

    # إزالة آخر سطر فاضي لو موجود
    while parts and not parts[-1].strip():
        parts.pop()

    return "\n".join(parts)# formatting.py
from typing import List, Dict

from config import ARABIC_ROLE_TITLES


def format_single_group(role_key: str, items: List[str]) -> str:
    """صياغة مجموعة واحدة (مثلاً تحديات التاجر) كنص جاهز للإرسال."""
    title = ARABIC_ROLE_TITLES.get(role_key, role_key)

    if not items:
        return f"⭐️ *{title}*\nلا توجد تحديات متاحة حاليًا لهذا الدور."

    lines = [f"⭐️ *{title}*"]
    lines.append("")  # سطر فاضي

    # نخلي نص التحدي الأصلي كما هو، ونضيف صيغة أمر بالعربي
    for i, text in enumerate(items, start=1):
        # مثال: "1. أنجز التحدي التالي: 5 Blackcurrants picked"
        lines.append(f"{i}. أنجز التحدي التالي:\n   {text}")

    return "\n".join(lines)


def format_full_all(groups: Dict[str, List[str]]) -> str:
    """صياغة رسالة كاملة فيها كل الأقسام (عام + كل الأدوار)."""
    order = ["general", "bounty", "trader", "collector", "moonshiner", "naturalist"]
    parts: List[str] = []

    header = (
        "🔥 *التحديات اليومية لليوم في Red Dead Online*\n\n"
        "كل سطر فيه صيغة أمر بالعربي مع نص التحدي الأصلي بالإنجليزي، "
        "حتى تبقى أسماء الحيوانات والنباتات كما هي 🌿🦬\n\n"
    )
    parts.append(header)

    for key in order:
        section = format_single_group(key, groups.get(key, []))
        parts.append(section)
        parts.append("")  # سطر فاصل

    # إزالة آخر سطر فاضي لو موجود
    while parts and not parts[-1].strip():
        parts.pop()

    return "\n".join(parts)
