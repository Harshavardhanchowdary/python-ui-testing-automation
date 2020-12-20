from collections import deque
import allure_commons
from allure_commons.reporter import AllureReporter
from allure_commons.utils import now
from allure_commons.utils import platform_label
from allure_commons.types import LabelType, AttachmentType
from allure_commons.model2 import TestResult
from allure_commons.model2 import Label
from allure_behave.utils import scenario_severity
from allure_behave.utils import scenario_tags
from allure_behave.utils import scenario_name
from ui_automation_core.utilities.allure.utils import scenario_parameters, scenario_history_id
from allure_behave.listener import AllureListener


class AllureCustomListener(AllureListener):
    def __init__(self, behave_config):
        super()
        self.behave_config = behave_config
        self.logger = AllureReporter()
        self.current_step_uuid = None
        self.execution_context = Context()
        self.fixture_context = Context()
        self.steps = deque()
        self.browser = behave_config.userdata['browser']

    @allure_commons.hookimpl
    def start_test(self, parent_uuid, uuid, name, parameters, context):
        scenario = context['scenario']
        self.fixture_context.enter()
        self.execution_context.enter()
        self.execution_context.append(uuid)
        test_case = TestResult(uuid=uuid, start=now())
        test_case.name = scenario_name(scenario)
        test_case.historyId = scenario_history_id(scenario, self.browser)
        test_case.description = '\n'.join(scenario.description)
        test_case.parameters = scenario_parameters(scenario, self.browser)
        test_case.labels.extend([Label(name=LabelType.TAG, value=tag) for tag in scenario_tags(scenario)])
        test_case.labels.append(Label(name=LabelType.SEVERITY, value=scenario_severity(scenario).value))
        test_case.labels.append(Label(name=LabelType.FEATURE, value=scenario.feature.name))
        test_case.labels.append(Label(name=LabelType.FRAMEWORK, value='behave'))
        test_case.labels.append(Label(name=LabelType.LANGUAGE, value=platform_label()))
        self.logger.schedule_test(uuid, test_case)


class Context(list):
    def __init__(self, _list=list()):
        super(Context, self).__init__(_list)
        self._stack = [_list]

    def enter(self, _list=list()):
        self._stack.append(self[:])
        self[:] = _list
        return self

    def exit(self):
        gone, self[:] = self[:], self._stack.pop()
        return gone
