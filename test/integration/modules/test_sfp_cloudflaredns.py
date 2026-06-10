import pytest
import unittest

from modules.sfp_cloudflaredns import sfp_cloudflaredns
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleIntegrationCloudflaredns(unittest.TestCase):

    def test_handleEvent_event_data_safe_internet_name_not_blocked_should_not_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_cloudflaredns()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_cloudflaredns)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'INTERNET_NAME'
        event_data = 'cloudflare.com'
        event_module = 'example module'
        source_event = evt

        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)

    def test_handleEvent_event_data_adult_internet_name_blocked_should_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_cloudflaredns()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'BLACKLISTED_INTERNET_NAME'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = 'CloudFlare - Family [pornhub.com]'
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_cloudflaredns)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'INTERNET_NAME'
        event_data = 'pornhub.com'
        event_module = 'example module'
        source_event = evt

        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))
