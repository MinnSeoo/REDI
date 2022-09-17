from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year
        self.date = f"{year}-{month:0>2}-{number:0>2}"

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = (
            "일",
            "월",
            "화",
            "수",
            "목",
            "금",
            "토",
        )
        self.months = (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(
                    number=day,
                    past=past,
                    month=self.month,
                    year=self.year,
                )
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
