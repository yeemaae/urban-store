from django.views.generic.base import TemplateView

from .forms import OrderForm


class OrderCreateView(TemplateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
