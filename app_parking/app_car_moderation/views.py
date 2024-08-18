from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ParkingRecord, Rate, Payment, CarList


# 5. Пошук номера авто у базі даних зареєстрованих транспортних засобів.
# 6. Відстеження тривалості паркування.


def search_car(request):
    query = request.GET.get("license_number")
    result = None
    owner = None
    if query:
        result = CarList.search_by_license_number(query)
        if result:
            owner = result.owner
    return render(
        request,
        "app_car_moderation/search_car.html",
        {"result": result, "owner": owner},
    )


# 7. Запис часу в'їзду/виїзду кожного разу, коли визначається номерний знак.
# 8. Розрахунок загальної тривалості паркування для кожного унікального номерного знаку.
# 9. Зберігання даних про тривалість, пов'язаних із номерними знаками в базі даних. Розрахунок вартості паркування.
# 10. Сповіщення користувача, якщо накопичені парковочні витрати перевищують встановлені ліміти.
# 11. Генерація звітів про розрахунки, які можна експортувати у форматі CSV.
