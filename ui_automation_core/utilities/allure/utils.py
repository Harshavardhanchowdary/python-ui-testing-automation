from allure_commons.model2 import Parameter
from allure_commons.utils import md5


def scenario_history_id(scenario, browser):
    parts = [scenario.feature.name, scenario.name]
    if scenario._row:
        row = scenario._row
        parts.extend(['{name}={value}'.format(name=name, value=value) for name, value in zip(row.headings, row.cells)])
    else:
        parts.extend([browser])
    return md5(*parts)


def scenario_parameters(scenario, browser):
    row = scenario._row
    return [Parameter(name=name, value=value) for name, value in zip(row.headings, row.cells)] if row else [
        {"name": "browser", "value": browser}]
