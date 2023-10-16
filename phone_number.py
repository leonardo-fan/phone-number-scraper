from phonenumbers import PhoneNumberMatcher, PhoneNumberFormat, \
                         region_code_for_country_code, format_number

# will get all phone number strings from text with a given country code
# if a match has a leading zero it will only be added if it is a valid number from the country code
# otherwise the number will only be added if it is a valid international number with +(country code)
# returns list of mobile number strings in international format
# docs: https://daviddrysdale.github.io/python-phonenumbers/phonenumbers.phonenumbermatcher.html 
def get_phone_numbers_from_string(text, country_code=61):
    # for each match, format number into international mobile string
    return [format_number(match.number, PhoneNumberFormat.INTERNATIONAL)
            for match in PhoneNumberMatcher(text, region_code_for_country_code(country_code))]
