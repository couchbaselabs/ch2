# -*- coding: utf-8 -*-
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

from __future__ import with_statement

import os
import sys
import logging
#import pymongo
from pprint import pprint,pformat
#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
import traceback
import time
import constants
import boto3
import uuid
import json
import io
import csv
from .abstractdriver import *

## ==============================================
## Awss3Driver
## ==============================================
class Awss3Driver(AbstractDriver):
    DEFAULT_CONFIG = {
        "host":         ("The hostname to mongod", "localhost" ),
        "port":         ("The port number to mongod", 27017 ),
        "name":         ("Collection name", "tpcc"),
        "denormalize":  ("If set to true, then the CUSTOMER data will be denormalized into a single document", False),
    }

    def __init__(self, ddl, clientId, TAFlag="T",
                 schema=constants.CH2_DRIVER_SCHEMA["CH2"],
                 preparedTransactionQueries={},
                 analyticalQueries=constants.CH2_DRIVER_ANALYTICAL_QUERIES["HAND_OPTIMIZED_QUERIES"],
                 customerExtraFields=constants.CH2_CUSTOMER_EXTRA_FIELDS["NOT_SET"],
                 ordersExtraFields=constants.CH2_ORDERS_EXTRA_FIELDS["NOT_SET"],
                 itemExtraFields=constants.CH2_ITEM_EXTRA_FIELDS["NOT_SET"],
                 load_mode=constants.CH2_DRIVER_LOAD_MODE["NOT_SET"],
                 load_format=constants.CH2_DRIVER_LOAD_FORMAT["JSON"],
                 kv_timeout=constants.CH2_DRIVER_KV_TIMEOUT,
                 bulkload_batch_size=constants.CH2_DRIVER_BULKLOAD_BATCH_SIZE):
        super(Awss3Driver, self).__init__("awss3", ddl)
        try:
            self.client_id = clientId;
            self.TAFlag = TAFlag
            self.schema = schema
            self.s3client = boto3.client('s3')
            if self.client_id == 0 and self.TAFlag == "L":
                self.s3client.create_bucket(Bucket=self.schema)
            self.denormalize = False
            self.analyticalQueries = analyticalQueries
            self.customerExtraFields = customerExtraFields
            self.ordersExtraFields = ordersExtraFields
            self.itemExtraFields = itemExtraFields
            self.bulkload_batch_size = bulkload_batch_size
            self.load_format = load_format

        except Exception as e:
            raise Exception(
                "The following error occurred: ", e)

        return

    ## ----------------------------------------------
    ## makeDefaultConfig
    ## ----------------------------------------------
    def makeDefaultConfig(self):
        return Awss3Driver.DEFAULT_CONFIG
    
    ## ----------------------------------------------
    ## loadConfig
    ## ----------------------------------------------
    def loadConfig(self, config):
        return

    def tryBulkLoad(self, tableName, cur_batch, key):
        for i in range(constants.NUM_LOAD_RETRIES):
            try:
                json_str = json.dumps(cur_batch)
                if self.load_format == constants.CH2_DRIVER_LOAD_FORMAT["CSV"]:
                    data = json.loads(json_str)
                    # Create a CSV writer in memory
                    output = io.StringIO()
                    writer = csv.writer(output)
                    # Write the header row
                    writer.writerow(data[0].keys())
                    # Write the data rows
                    for row in data:
                        writer.writerow(row.values())
                    # Get the CSV string
                    csv_str = output.getvalue()
                    self.s3client.put_object(Bucket=self.schema, Key=tableName+"/"+tableName+ "."+key+".csv", Body=csv_str,)
                else:
                    self.s3client.put_object(Bucket=self.schema, Key=tableName+"/"+tableName+ "."+key+".json", Body=json_str,)                    
                return True
            except:
                logging.debug("Client ID # %d exception bulk load data, try %d" % (self.client_id, i))
                exc_info = sys.exc_info()
                tb = ''.join(traceback.format_tb(exc_info[2]))
                logging.debug(f'Exception info: {exc_info[1]}\nTraceback:\n{tb}')
                time.sleep(1)

        logging.debug("Client ID # %d failed bulk load data after %d retries" % (self.client_id, constants.NUM_LOAD_RETRIES))
        return False

    ## ----------------------------------------------
    ## loadTuples for aws s3
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        if len(tuples) == 0:
            return

        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        assert tableName in constants.ALL_TABLES, "Unexpected table %s" % tableName

        # For bulk load: load in batches
        cur_batch = []
        cur_size = 0
        for t in tuples:
            key, val = self.getOneDoc(tableName, t, True)
            cur_batch.append(val)
            cur_size += 1
            if cur_size >= 10000: #self.bulkload_batch_size:
                result = self.tryBulkLoad(tableName, cur_batch, key)
                if result == True:
                    cur_batch = []
                    cur_size = 0
                    continue
                else:
                    logging.debug("Client ID # %d failed bulk load data, aborting..." % self.client_id)
        if cur_size > 0:
            result = self.tryBulkLoad(tableName, cur_batch, key)
            if result == False:
                logging.debug("Client ID # %d failed bulk load data, aborting..." % self.client_id)
        return

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Client ID # %d Finished loading tables" % (self.client_id))
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            for name in constants.ALL_TABLES:
                logging.debug("%-12s%d records" % (name+":", self.database[name].count_documents({})))
        ## IF

## CLASS
