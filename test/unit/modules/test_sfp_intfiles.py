import pytest
import unittest

from modules.sfp_intfiles import sfp_intfiles
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleIntfiles(unittest.TestCase):

    def test_opts(self):
        module = sfp_intfiles()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = NecroSpider(self.default_options)
        module = sfp_intfiles()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_intfiles()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_intfiles()
        self.assertIsInstance(module.producedEvents(), list)

    def test_handleEvent_event_data_internal_url_with_interesting_file_extension_should_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_intfiles()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'INTERESTING_FILE'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = 'https://necrospider.net/example.zip'
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_intfiles)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'LINKED_URL_INTERNAL'
        event_data = 'https://necrospider.net/example.zip'
        event_module = 'example module'
        source_event = evt

        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))

    def test_handleEvent_event_data_internal_url_without_interesting_file_extension_should_not_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_intfiles()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_intfiles)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'LINKED_URL_INTERNAL'
        event_data = 'https://necrospider.net/example'
        event_module = 'example module'
        source_event = evt

        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)
