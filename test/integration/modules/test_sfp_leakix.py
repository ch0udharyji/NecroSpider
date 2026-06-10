import pytest
import unittest

from modules.sfp_leakix import sfp_leakix
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleIntegrationleakix(unittest.TestCase):

    @unittest.skip("todo")
    def test_handleEvent(self):
        sf = NecroSpider(self.default_options)

        module = sfp_leakix()
        module.setup(sf, dict())

        target_value = 'example target value'
        target_type = 'IP_ADDRESS'
        target = NecroSpiderTarget(target_value, target_type)
        module.setTarget(target)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = NecroSpiderEvent(event_type, event_data, event_module, source_event)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
