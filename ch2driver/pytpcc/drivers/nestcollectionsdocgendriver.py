# / -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http://www.cs.brown.edu/~pavlo/
#
# Original Java Version:
# Copyright (C) 2008
# Evan Jones
# Massachusetts Institute of Technology
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------

import logging
from pathlib import Path

import ujson

import constants
from .abstractdriver import AbstractDriver


## ==============================================
## NestcollectionsDocGenDriver
## ==============================================
class NestcollectionsdocgenDriver(AbstractDriver):
    DEFAULT_CONFIG = {
        "output_dir": (
            "The path to the directory to store the JSON files",
            "/tmp/ch2_data",
        ),
    }

    def __init__(
        self,
        ddl,
        clientId,
        schema=constants.CH2_DRIVER_SCHEMA["CH2"],
        customerExtraFields=constants.CH2_CUSTOMER_EXTRA_FIELDS["NOT_SET"],
        ordersExtraFields=constants.CH2_ORDERS_EXTRA_FIELDS["NOT_SET"],
        itemExtraFields=constants.CH2_ITEM_EXTRA_FIELDS["NOT_SET"],
        bulkload_batch_size=constants.CH2_DRIVER_BULKLOAD_BATCH_SIZE,
        *args,
        **kwargs,
    ):
        super().__init__("nestcollectionsdocgen", ddl)
        self.client_id = clientId
        self.schema = schema
        self.bulkload_batch_size = bulkload_batch_size

        self.customerExtraFields = customerExtraFields
        self.ordersExtraFields = ordersExtraFields
        self.itemExtraFields = itemExtraFields

        self.batches = {tableName: [0, [], 0] for tableName in constants.ALL_TABLES}

    ## ----------------------------------------------
    ## makeDefaultConfig
    ## ----------------------------------------------
    def makeDefaultConfig(self):
        return self.DEFAULT_CONFIG

    ## ----------------------------------------------
    ## loadConfig
    ## ----------------------------------------------
    def loadConfig(self, config):
        self.output_dir = Path(config["output_dir"])
        assert self.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return

    def saveTuples(self, tableName: str, tuples: list[dict], batch_idx: int) -> bool:
        filename = self.output_dir / (
            "%s-%d-%d.json"
            % (
                tableName,
                self.client_id,
                batch_idx,
            )
        )
        try:
            with open(filename, "w") as f:
                f.writelines(tuples)
        except Exception as e:
            logging.error("Error saving tuples to file: %s" % str(e))
            return False

        return True

    ## ----------------------------------------------
    ## loadTuples for Couchbase (Adapted from MongoDB implemenetation).
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        if len(tuples) == 0:
            return

        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        assert tableName in constants.ALL_TABLES, "Unexpected table %s" % tableName

        batch_idx, cur_batch, batch_size = self.batches[tableName]
        # For bulk load: load in batches
        for t in tuples:
            key, val = self.getOneDoc(tableName, t, generateKey=True)
            val["key"] = key
            json_val = ujson.dumps(val) + "\n"
            cur_batch.append(json_val)
            batch_size += len(json_val)
            if batch_size > self.bulkload_batch_size:
                result = self.saveTuples(tableName, cur_batch, batch_idx)
                if result:
                    batch_idx += 1
                    cur_batch = []
                    batch_size = 0
                    continue
                else:
                    logging.debug(
                        "Client ID # %d failed bulk load data into KV, aborting..."
                        % self.client_id
                    )

        self.batches[tableName] = [batch_idx, cur_batch, batch_size]

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Client ID # %d Writing last batches to disk" % (self.client_id))
        for tableName, (batch_idx, cur_batch, _) in self.batches.items():
            if cur_batch:
                self.saveTuples(tableName, cur_batch, batch_idx)

        logging.info("Client ID # %d Finished loading tables" % (self.client_id))
        return


## CLASS
