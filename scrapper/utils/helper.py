from datetime import datetime, timedelta

DATE_STR_FORMAT = "%m/%d/%Y"
DATE_FORMAT = "%d%m%Y"


def generate_action(action, target, input_text=None):
    """
    A helper function used to generate action dictionary.
    Idea for creating a separate function is that, it will make to avoid typo error in dict keys
    """
    return {
        "action": action,
        "target": target,
        "input_text": input_text
    }


def generate_date_range(num_of_months=0):
    current_date = datetime.now()
    end_month = current_date.month
    end_year = current_date.year

    if num_of_months == 0 or num_of_months == 1:
        # Current month news filter
        return (datetime.strptime(f"02{end_month}{end_year}", DATE_FORMAT).strftime(DATE_STR_FORMAT),
                datetime.strptime(f"{current_date.day}{end_month}{end_year}", DATE_FORMAT).strftime(DATE_STR_FORMAT)
                )

    start_date = datetime.now() - timedelta(weeks=4 * num_of_months)
    start_month = start_date.month
    start_year = start_date.year

    return (
        datetime.strptime(f"02{start_month}{start_year}", DATE_FORMAT).strftime(DATE_STR_FORMAT),
        datetime.strptime(f"{current_date.day}{end_month}{end_year}", DATE_FORMAT).strftime(DATE_STR_FORMAT)
    )
