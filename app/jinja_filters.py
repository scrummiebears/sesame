def whatInput(form_field):
    if form_field.name in ["start_date", "end_date", "departure_date"]:
        return "date"
    return None