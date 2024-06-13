from locale import currency
from django import template
from django.db.models import Q
from settings.models import Currency, Settings, FooterLinks
from django.contrib.auth.models import Permission
from django.contrib.staticfiles.finders import find as find_static_file


register = template.Library()


@register.simple_tag
def currencies():
	cur = Currency.objects.all().values_list('code', flat=True)
	return cur
# register.filter('currencies', Currencies)

@register.simple_tag
def DefaultCurrency():
	mycurrency = Settings.objects.all().first()
	if mycurrency is not None:
		currency = mycurrency.default_currency
		return [currency.code, currency.rate, currency.symbol_native]
	else:
		return 'UGX'

# @register.simple_tag(takes_context=True)
# def mycurrency(context):
#     currency = context['request'].COOKIES['currency']
#     get_currency = Currency.objects.get(code = currency)
#     return [currency, get_currency.rate, get_currency.symbol_native]

@register.simple_tag(takes_context=True)
def mycurrency(context):
	try:
		get_currency = Currency.objects.get(code = context['request'].COOKIES['mycurrency'])
		exists = True
		return [get_currency.rate, get_currency.symbol_native, exists]
	except:
		my_currency = Settings.objects.filter().first()
		if my_currency is not None:
			get_currency = my_currency.default_currency
			exists = False
			return [get_currency.rate, get_currency.symbol_native, exists]

@register.filter
def FLinks(value):
	link_list = FooterLinks.objects.filter(section_name=value).first().links.all()
	return link_list
register.filter('footerlink', FLinks)

@register.simple_tag
def footerlinks():
	flinks = FooterLinks.objects.all()
	return flinks

@register.filter
def intformat(value, length):
	if len(str(value)) < length:
		no_zero = length - len(str(value))
		return '0'*no_zero+str(value)
	else:
		return value
register.filter('intformat', intformat)

@register.filter
def multiplication(value1, value2):
	result = float(value1) * float(value2)
	return result
register.filter('mult', multiplication)

@register.filter
def getperms(value):
	return Permission.objects.filter(content_type = value)
register.filter('getperms', getperms)


