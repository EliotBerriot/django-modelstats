from django.db import models


class Reporter(object):
    config = []

    def __init__(self, *args, **kwargs):

        for config_key, default_value in self.config:
            setattr(self, config_key, kwargs.get(config_key, default_value))

    def get_config(self, **kwargs):
        config = {}
        for config_key, default_value in self.config:
            config[config_key] = kwargs.get(config_key, getattr(self, config_key))
        return config

    def process(self, queryset, **kwargs):
        config = self.get_config(**kwargs)
        report = {}
        report['data'] = self.get_report_content(queryset, **config)
        return report

    def get_report_content(self, queryset, **kwargs):
        return None


class DateTimeReporter(Reporter):
    config = [
        ('datetime_field', None),
        ('group_by', 'day'),
    ]

    def get_report_content(self, queryset, **kwargs):
        return queryset.extra(select={kwargs['group_by']: 'date({0})'.format(kwargs['datetime_field'])}) \
                       .values(kwargs['group_by']) \
                       .annotate(total=models.Count(kwargs['datetime_field']))