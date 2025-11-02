from .models import HeaderSettings, NavMenu

def header_context(request):
    settings = HeaderSettings.objects.first()
    menu_items = NavMenu.objects.order_by("order")
    return {
        "header_settings": settings,
        "menu_items": menu_items,
    }