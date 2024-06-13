from django import template

register = template.Library()


# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, '')


# @register.filter
# def lower(value):
#     return value.lower()
@register.filter(name='password_protect')
def protect(value):
    return "*" * (len(value) // 8)


@register.filter(name='email_protect')
def protect(value):
    email_1 = value.split('@')
    email_2 = email_1[0][(len(email_1[0]) // 2):-1]
    new_email = email_1[0][:(len(email_1[0]) // 2)] + ('*' * len(email_2)) + email_1[1]
    return new_email


@register.filter(name='rel_filter')
def edit(value):
    return value.replace('_', ' ')


@register.filter(name='convert_time_comment')
def convert_time_comment(date):
    date_1 = date.split(' ')[0]
    date_2 = date.split(' ')[1].split('.')[0]
    month = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'Jume',
        '07': 'July',
        '08': 'AUgust',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }
    split_date_1 = date_1.split('-')
    split_date_2 = date_2.split(':')
    Final_date = f'{split_date_1[2]} {month[split_date_1[1]]} {split_date_1[0]} г. {split_date_2[0]}:{split_date_2[1]}'
    return Final_date
