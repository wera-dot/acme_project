from django.shortcuts import render

from .forms import BirthdayForm
from .utils import calculate_birthday_countdown


def bbirthday(request):
    # print(request.GET)  # Напечатаем. 
    if request.GET:
        form = BirthdayForm(request.GET)
        if form.is_valid():
            # считаем, сколько дней осталось до дня рождения.
            pass
    else:
        form = BirthdayForm()
    context = {'form': form}
    # return render(request, 'birthday/birthday.html', context=context)
    return render(request, 'birthday/birthday.html', context)


def birthday(request):
    form = BirthdayForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)
