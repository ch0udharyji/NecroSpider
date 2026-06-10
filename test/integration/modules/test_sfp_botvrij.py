import pytest
import unittest

from modules.sfp_botvrij import sfp_botvrij
from sflib import NecroSpider
from necrospider import NecroSpiderEvent, NecroSpiderTarget


@pytest.mark.usefixtures
class TestModuleIntegrationBotvrij(unittest.TestCase):

    @unittest.skip("todo")
    def test_handleEvent(self):
        sf = NecroSpider(self.default_options)

        module = sfp_botvrij()
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
