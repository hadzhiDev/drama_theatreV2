from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.models import Ticket
from utils.models import TimeStampAbstractModel


class Cart(TimeStampAbstractModel):
    MAN = 'man'
    WOMEN = 'women'

    SEX = (
        (MAN, 'Мужчина'),
        (WOMEN, 'Женщина')
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    name = models.CharField('имя и фамилия', max_length=140)
    email = models.EmailField('электронная почта')
    phone = PhoneNumberField('номер телефона')
    sex = models.CharField(max_length=100, choices=SEX, verbose_name='пол')
    date_of_birth = models.DateField(verbose_name='дата рождения')
    user = models.ForeignKey('account.User', models.CASCADE, 'carts', verbose_name='пользователь',
                             null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return sum(ticket.price for ticket in self.tickets.all())


class TicketForSale(models.Model):

    class Meta:
        verbose_name = 'билет на продажу'
        verbose_name_plural = 'билеты на продажу'

    cart = models.ForeignKey('cart.Cart', models.CASCADE, 'tickets', verbose_name='корзина')
    ticket = models.ForeignKey('core.Ticket', models.PROTECT, verbose_name='билет')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.ticket}'

    def clean(self):
        ticket = Ticket.objects.get(id=self.ticket.id)
        ticket.is_sold = True
        ticket.save()