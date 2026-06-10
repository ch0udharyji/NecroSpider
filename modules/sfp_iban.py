# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_iban
# Purpose:      NecroSpider plug-in for scanning retrieved content by other
#               modules (such as sfp_spider) and identifying IBANs.
#
# Author:      Krishnasis Mandal <krishnasis@hotmail.com>
#
# Created:     26/04/2020
# Copyright:   (c) Steve Micallef
# Licence:     MIT
# -------------------------------------------------------------------------------

from necrospider import NecroSpiderEvent, NecroSpiderHelpers, NecroSpiderPlugin


class sfp_iban(NecroSpiderPlugin):

    meta = {
        'name': "IBAN Number Extractor",
        'summary': "Identify International Bank Account Numbers (IBANs) in any data.",
        'flags': ["errorprone"],
        'useCases': ["Footprint", "Investigate", "Passive"],
        'categories': ["Content Analysis"]
    }

    opts = {
    }

    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        # Override datasource for sfp_iban module
        self.__dataSource__ = "Target Website"

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["TARGET_WEB_CONTENT", "DARKNET_MENTION_CONTENT",
                "LEAKSITE_CONTENT"]

    # What events this module produces
    def producedEvents(self):
        return ["IBAN_NUMBER"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        self.debug(f"Received event, {eventName}, from {srcModuleName}")

        ibans = NecroSpiderHelpers.extractIbansFromText(eventData)
        for ibanNumber in set(ibans):
            self.info(f"Found IBAN number: {ibanNumber}")
            evt = NecroSpiderEvent("IBAN_NUMBER", ibanNumber, self.__name__, event)
            if event.moduleDataSource:
                evt.moduleDataSource = event.moduleDataSource
            else:
                evt.moduleDataSource = "Unknown"
            self.notifyListeners(evt)

# End of sfp_iban class
