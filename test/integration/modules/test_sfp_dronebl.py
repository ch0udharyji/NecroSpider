import pytest
import unittest

from modules.sfp_dronebl import sfp_dronebl
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleIntegrationDronebl(unittest.TestCase):

    def test_handleEvent_event_data_safe_ip_address_not_blocked_should_not_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_dronebl()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_dronebl)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'IP_ADDRESS'
        event_data = '1.0.0.1'
        event_module = 'example module'
        source_event = evt

        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)
