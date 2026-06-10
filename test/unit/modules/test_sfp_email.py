import pytest
import unittest

from modules.sfp_email import sfp_email
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleEmail(unittest.TestCase):

    def test_opts(self):
        module = sfp_email()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = NecroSpider(self.default_options)
        module = sfp_email()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_email()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_email()
        self.assertIsInstance(module.producedEvents(), list)

    @unittest.skip("todo")
    def test_handleEvent_event_data_target_web_content_containing_email_address_should_return_event(self):
        sf = NecroSpider(self.default_options)

        module = sfp_email()
        module.setup(sf, dict())

        target_value = 'necrospider.net'
        target_type = 'INTERNET_NAME'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'EMAILADDR'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = 'firstname.lastname@necrospider.net'
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_email)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        event_type = 'TARGET_WEB_CONTENT'
        event_data = '<p>sample data firstname.lastname@necrospider.net sample data.</p>'
        event_module = 'example module'
        source_event = evt
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))
