from datetime import date

def current_year():

    return date.today().year

def is_current_year(ano:int)->bool:

    return ano == current_year()

def current_month():

    return date.today().month