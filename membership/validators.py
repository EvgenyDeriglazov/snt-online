# Field data validators for membership application

def validate_number(value):
    """Makes number validation (only numeric symbols)."""
    wrong_char_list = []
    for char in value:
        if ord(char) > 57 or ord(char) < 48:
            wrong_char_list.append(char)
    if wrong_char_list:
        wrong_string = ", ".join(wrong_char_list)
        raise ValidationError(
            _('Некорректный символ - (' + wrong_string + ')')
        )

def validate_year_period_min_length(value):
	if len(value) < 4:
		raise ValidationError(
			_('Укажите год в виде 4-х значного числа')
			)