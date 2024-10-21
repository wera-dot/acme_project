from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView #, TemplateView
)

from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown





def bbirthday(request):
    # print(request.GET)  # Напечатаем. 
    # if request.GET:
    if request.POST:
        # form = BirthdayForm(request.GET)
        form = BirthdayForm(request.POST)
        if form.is_valid():
            # считаем, сколько дней осталось до дня рождения.
            pass
    else:
        form = BirthdayForm()
    context = {'form': form}
    # return render(request, 'birthday/birthday.html', context=context)
    return render(request, 'birthday/birthday.html', context)


def birthdayy(request, pk=None):
    # form = BirthdayForm(request.GET or None)
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(request.POST or None, files=request.FILES or None, instance=instance)
    # form = BirthdayForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # birthdays = Birthday.objects.all()
    birthdays = Birthday.objects.order_by('id')
    paginator = Paginator(birthdays, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # context = { 'birthdays': birthdays}
    context = { 'page_obj': page_obj }
    
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    # return render(request, 'birthday/birthday.html', context)
    return render(request, 'birthday/bbbirthday_form.html', context)


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10
    # template_name
    # get_context_data()


class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')

    # def __init__(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     super().__init__(*args, **kwargs)


class BirthdayCreateView(BirthdayMixin, CreateView):
    pass
    # form_class = BirthdayForm
    # model = Birthday
    # # fields = '__all__'
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'   # по умолчанию будет искать birthday_form.html
    # # success_url = reverse_lazy('birthday:list')


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    pass
    # form_class = BirthdayForm
    # model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')


class BirthdayDeleteView(DeleteView):
    # pass
    model = Birthday
    # template_name = 'birthday/bbbirthday_form.html'   
    # template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
