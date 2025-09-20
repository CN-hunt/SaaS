from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    """重写该发方法"""
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'
