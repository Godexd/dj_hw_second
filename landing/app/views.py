from collections import Counter

from django.shortcuts import render
# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter({'orig': 0, 'test': 0})
counter_click = Counter({'from_orig': 0, 'from_test': 0})


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    argument = request.GET.get('from-landing')
    if argument == 'original':
        counter_click['from_orig'] += 1
    elif argument == 'test':
        counter_click['from_test'] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    argument = request.GET.get('ab-test-arg')
    if argument == 'original':
        url = 'landing.html'
        counter_show['orig'] += 1
    elif argument == 'test':
        url = 'landing_alternate.html'
        counter_show['test'] += 1
    else:
        url = 'landing.html'
    return render(request, url)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_show['orig']:
        original_conversion = counter_click['from_orig']/counter_show['orig']
    else:
        original_conversion = 0
    if counter_show['test']:
        test_conversion = counter_click['from_test']/counter_show['test']
    else:
        test_conversion = 0
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
