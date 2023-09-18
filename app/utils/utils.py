def format_date(date_obj):
    """Helper function to format date objects."""
    return date_obj.strftime('%a, %d %b %Y') if date_obj else None
