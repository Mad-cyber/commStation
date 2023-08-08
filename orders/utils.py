import datetime


def generate_order_number(pk):
    #https://www.programiz.com/python-programming/datetime/strftime
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%S')#yearmonthday format for the order
    order_number = current_datetime + str(pk)

    return order_number
