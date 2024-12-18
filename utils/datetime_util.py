from datetime import datetime

month_map = {
    'جنوری': 'Jan',
    'فروری': 'Feb',
    'مارچ': 'March',
    'اپریل': 'Apr',
    'مئی': 'May',
    'جون': 'June',
    'جولائی': 'July',
    'اگست': 'Aug',
    'ستمبر': 'Sep',
    'اکتوبر': 'Oct',
    'نومبر': 'Nov',
    'دسمبر': 'Dec'
}

def convert_urdu_date(urdu_date):
    # Split the Urdu date string into day, month, and year
    day, month, year = urdu_date.split()
    
    # Replace Urdu month with the English month
    if month in month_map:
        english_month = month_map[month]
        english_date = f"{english_month} {day}, {year}"
        return english_date
    else:
        raise ValueError("Month not recognized in Urdu.")

def convert_to_datetime(d):

    converted_date = ''

    try:
            # Attempt to parse the date string using the given format
            converted_date = datetime.strptime(d, "%b %d, %Y")
    
    except ValueError:
        try:
            # Attempt to parse date in Urdu
            english_date = convert_urdu_date(d)
            # Now, parse the English date using datetime
            converted_date = datetime.strptime(english_date, "%b %d, %Y")

        except ValueError as e:
            print("Error:", e)
            print(d)

    return converted_date