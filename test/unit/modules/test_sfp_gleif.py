import pytest
import unittest

from modules.sfp_gleif import sfp_gleif
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleGleif(unittest.TestCase):

    def test_opts(self):
        module = sfp_gleif()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = NecroSpider(self.default_options)
        module = sfp_gleif()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_gleif()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_gleif()
        self.assertIsInstance(module.producedEvents(), list)

    def test_handleEvent_event_data_invalid_lei_should_not_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_gleif()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_gleif)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'LEI'
        event_data = 'invalid LEI'
        event_module = 'example module'
        source_event = evt
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)
