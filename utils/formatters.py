"""
Price formatting utilities
"""

def format_vnd_price(price: float, use_k_notation: bool = True) -> str:
    """Format VND price with optional k notation"""
    if use_k_notation and price >= 1000:
        return f"{price/1000:,.1f}k VND"
    else:
        return f"{price:,.0f} VND"

def format_vnd_price_large(price: float) -> str:
    """Format large VND prices with M/k notation"""
    if price > 1000000:
        return f"{price/1000000:,.1f}M VND"
    elif price > 1000:
        return f"{price/1000:,.0f}k VND"
    else:
        return f"{price:,.0f} VND"

def format_usd_price(price: float) -> str:
    """Format USD price"""
    return f"${price:,.2f}"

def format_percentage(value: float, include_sign: bool = True) -> str:
    """Format percentage with optional sign"""
    if include_sign:
        sign = "+" if value >= 0 else ""
        return f"{sign}{value:.2f}%"
    else:
        return f"{value:.2f}%"

def clean_numeric_string(value: str) -> float:
    """Clean numeric string by removing commas and converting to float"""
    if value == 'N/A' or not value:
        return 0.0
    
    try:
        cleaned = str(value).replace(',', '')
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0