#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http:##www.cs.brown.edu/~pavlo/
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

import sys
import traceback
import os
import string
import datetime
import logging
import re
import argparse
import glob
import time
import multiprocessing
from configparser import SafeConfigParser
from pprint import pprint,pformat
import constants
from util import *
from runtime import *
import drivers
from random import randint

logging.basicConfig(level = logging.INFO,
                    format="%(asctime)s [%(funcName)s:%(lineno)03d] %(levelname)-5s: %(message)s",
                    datefmt="%m-%d-%Y %H:%M:%S",
                    stream = sys.stdout)

## ==============================================
## createDriverClass
## ==============================================
def createDriverClass(name):
    full_name = "%sDriver" % name.title()
    mod = __import__('drivers.%s' % full_name.lower(), globals(), locals(), [full_name])
    klass = getattr(mod, full_name)
    return klass
## DEF

## ==============================================
## getDrivers
## ==============================================
def getDrivers():
    drivers = [ ]
    for f in map(lambda x: os.path.basename(x).replace("driver.py", ""), glob.glob("./drivers/*driver.py")):
        if f != "abstract": drivers.append(f)
    return (drivers)
## DEF

## ==============================================
## startLoading
## ==============================================
def startLoading(driverClass, scaleParameters, args, configi, load_mode, kv_timeout, bulkload_batch_size):
    numClients = args['tclients'] + args['aclients']
    logging.debug("Creating client pool with %d processes" % numClients)
    pool = multiprocessing.Pool(numClients)
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)

    # Split the warehouses into chunks
    w_ids = list(map(lambda x: [ ], range(numClients)))
    for w_id in range(scaleParameters.starting_warehouse, scaleParameters.ending_warehouse+1):
        idx = int(w_id % numClients)
        w_ids[idx].append(w_id)
    ## FOR

    loader_results = [ ]
    for i in range(numClients):
        r = pool.apply_async(loaderFunc, (i, driverClass, scaleParameters, args, config, w_ids[i], load_mode, kv_timeout, bulkload_batch_size, True))
        loader_results.append(r)
    ## FOR

    pool.close()
    logging.debug("Waiting for %d loaders to finish" % numClients)
    pool.join()
## DEF

## ==============================================
## loaderFunc
## ==============================================
def loaderFunc(clientId, driverClass, scaleParameters, args, config, w_ids, load_mode, kv_timeout, bulkload_batch_size, debug):
    driver = driverClass(args['ddl'], clientId, "L", load_mode, kv_timeout, bulkload_batch_size)
    assert driver != None
    logging.debug("Starting client execution: %s [warehouses=%d]" % (driver, len(w_ids)))

    config['load'] = True
    config['execute'] = False
    config['reset'] = False
    driver.loadConfig(config)

    try:
        loadItems = (1 in w_ids)
        l = loader.Loader(driver, scaleParameters, w_ids, loadItems)
        driver.loadStart()
        l.execute()
        driver.loadFinish()
    except KeyboardInterrupt:
        return -1
    except (Exception, AssertionError) as ex:
        logging.warning("Failed to load data: %s" % (ex))
        traceback.print_exc(file=sys.stdout)
        raise

## DEF

## ==============================================
## startExecution
## ==============================================
def startExecution(driverClass, qDone, warmupDurationQ, warmupDuration, warmupQueryIterations, scaleParameters, args, config):
    numTClients = args['tclients']
    numAClients = args['aclients']
    numClients = numTClients + numAClients
    logging.debug("Creating client pool with %d processes" % numClients)

    pool = multiprocessing.Pool(numClients)
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)

    worker_results = [ ]
    for i in range(numClients):
        #random_num = randint(1, 20)
        #time.sleep(round((random_num*0.1),2))
        print('')
        if i < numAClients:
            TAFlag = "A"
        else:
            TAFlag = "T"

        r = pool.apply_async(executorFunc, (i, TAFlag, driverClass, qDone, warmupDurationQ, warmupDuration, warmupQueryIterations, numAClients, scaleParameters, args, config, debug))
        worker_results.append(r)

    ## FOR

    pool.close()

    pool.join()

    total_results = results.Results(warmupDuration, warmupQueryIterations)

    for asyncr in worker_results:
        asyncr.wait()
        r = asyncr.get()
        assert r != None, "No results object returned!"
        if type(r) == int and r == -1: sys.exit(1)
        total_results.warmupDuration = r.warmupDuration
        total_results.warmupQueryIterations = r.warmupQueryIterations
        total_results.append(r)
    ## FOR

    return (total_results)
## DEF

## ==============================================
## executorFunc
## ==============================================
def executorFunc(clientId, TAFlag, driverClass, qDone, warmupDurationQ, warmupDuration, warmupQueryIterations, numAClients, scaleParameters, args, config, debug):
    driver = driverClass(args['ddl'], clientId, TAFlag)
    assert driver != None
    logging.debug("Starting client execution: %s" % driver)

    config['execute'] = True
    config['reset'] = False
    driver.loadConfig(config)
    e = executor.Executor(clientId, driver, qDone, warmupDurationQ, scaleParameters, TAFlag, warmupDuration, warmupQueryIterations, stop_on_error=args['stop_on_error'])
    driver.executeStart()
    results = e.execute(args['duration'], args['query_iterations'], warmupDuration, warmupQueryIterations, numAClients)
    driver.executeFinish()

    return results
## DEF

## ==============================================
## main
## ==============================================
if __name__ == '__main__':
    aparser = argparse.ArgumentParser(description='Python implementation of the TPC-C Benchmark')
    aparser.add_argument('system', choices=getDrivers(),
                         help='Target system driver')
    aparser.add_argument('--userid',
                         help='userid for couchbase', default = "Administrator")
    aparser.add_argument('--password',
                         help='password for couchbase', default = "password")
    aparser.add_argument('--query-url',
                         help='query-url <ip>:port', default = "127.0.0.1:8093")
    aparser.add_argument('--multi-query-url',
                         help = 'multi-query-url <ip>:port', default = "127.0.0.1:8093")
    aparser.add_argument('--data-url',
                         help='data-url <ip>', default = "127.0.0.1")
    aparser.add_argument('--multi-data-url', help = 'multi-data-url <ip>', default = "127.0.0.1")
    aparser.add_argument('--analytics-url',
                         help='analytics-url <ip>:port', default = "127.0.0.1:8095")
    aparser.add_argument('--config', type=argparse.FileType('r'),
                         help='Path to driver configuration file')
    aparser.add_argument('--reset', action='store_true',
                         help='Instruct the driver to reset the contents of the database')
    aparser.add_argument('--scalefactor', default=1, type=float, metavar='SF',
                         help='Benchmark scale factor')
    aparser.add_argument('--warehouses', default=4, type=int, metavar='W',
                         help='Number of Warehouses')
    aparser.add_argument('--duration', type=int, metavar='D',
                         help='How long to run the benchmark in seconds')
    aparser.add_argument('--warmup-duration', type=int, metavar='WD',
                         help='Warm up duration of the benchmark in seconds')
    aparser.add_argument('--query-iterations', type=int, metavar='QI',
                         help='How many iterations of the queries to run')
    aparser.add_argument('--warmup-query-iterations', type=int, metavar='WQI',
                         help='Number of warmup iterations of the queries to run')
    aparser.add_argument('--ddl', default=os.path.realpath(os.path.join(os.path.dirname(__file__), "tpcc.sql")),
                         help='Path to the TPC-C DDL SQL file')
    aparser.add_argument('--tclients', default=0, type=int, metavar='TC',
                         help='The number of blocking transaction clients to fork')
    aparser.add_argument('--aclients', default=0, type=int, metavar='AC',
                         help='The number of blocking analytics clients to fork')
    aparser.add_argument('--stop-on-error', action='store_true',
                         help='Stop the transaction execution when the driver throws an exception.')
    aparser.add_argument('--no-load', action='store_true',
                         help='Disable loading the data')
    aparser.add_argument('--no-execute', action='store_true',
                         help='Disable executing the workload')
    aparser.add_argument('--datasvc-bulkload', action='store_true',
                         help='Enable bulk loading the data through the data service')
    aparser.add_argument('--kv-timeout', type=int,
                         help='KV timeout for loading the data through the data service')
    aparser.add_argument('--bulkload-batch-size', type=int,
                         help='Batch size for bulk loading the data through the data service')
    aparser.add_argument('--datasvc-load', action='store_true',
                         help='Enable loading the data through the data service')
    aparser.add_argument('--qrysvc-load', action='store_true',
                         help='Enable loading the data through the query service')
    aparser.add_argument('--print-config', action='store_true',
                         help='Print out the default configuration file for the system and exit')
    aparser.add_argument('--debug', action='store_true',
                         help='Enable debug log messages')
    aparser.add_argument('--durability_level',
                         help='durability level', default="persistToMajority")
    aparser.add_argument('--txtimeout', metavar='TXTO', type=float, default=3,
                         help='txtimeout number in sec(ex: 2.5)')
    aparser.add_argument('--scan_consistency', metavar='not_bounded', default="not_bounded",
                         help='not_bounded,request_plus')
    aparser.add_argument('--run-date',
                         help='run date for TPCC data', default = "2021-01-01 00:00:00")
    args = vars(aparser.parse_args())
    print (args)
    if args['debug']: logging.getLogger().setLevel(logging.DEBUG)
    query_url = "127.0.0.1:8093"
    multi_query_url = "127.0.0.1:8093"
    data_url = "127.0.0.1"
    multi_data_url = "127.0.0.1"
    analytics_url = "127.0.0.1:8095"
    userid = "Administrator"
    password = "password"

    if args['query_url']:
        query_url = args['query_url']
    os.environ["QUERY_URL"] = query_url
    if args['multi_query_url']:
        multi_query_url = args['multi_query_url']
    os.environ["MULTI_QUERY_URL"] = multi_query_url
    if args['data_url']:
        data_url = args['data_url']
    os.environ["DATA_URL"] = data_url
    if args['multi_data_url']:
        multi_data_url = args['multi_data_url']
    os.environ["MULTI_DATA_URL"] = multi_data_url
    if args['analytics_url']:
        analytics_url = args['analytics_url']
    os.environ["ANALYTICS_URL"] = analytics_url
    if args['durability_level']:
        durability_level = args['durability_level']
        os.environ["DURABILITY_LEVEL"] = durability_level
    if args['txtimeout']:
        os.environ["TXTIMEOUT"] = str(args['txtimeout'])
    if args['scan_consistency']:
        os.environ["SCAN_CONSISTENCY"] = args['scan_consistency']
    if args['userid']:
        userid = args['userid']
    os.environ["USER_ID"] = userid
    if args['password']:
        password = args['password']
    os.environ["PASSWORD"] = password
    if args['run_date']:
        run_date = args['run_date']
        os.environ["RUN_DATE"] = str(run_date)
    load_mode = constants.CH2_DRIVER_LOAD_MODE["NOT_SET"]
    if args['datasvc_bulkload']:
        if load_mode == constants.CH2_DRIVER_LOAD_MODE["NOT_SET"]:
            load_mode = constants.CH2_DRIVER_LOAD_MODE["DATASVC_BULKLOAD"]
        else:
            logging.info("Cannot specify multiple types of load")
            sys.exit(0)
        if args['bulkload_batch_size']:
            bulkload_batch_size = args['bulkload_batch_size']
        else:
            bulkload_batch_size = constants.CH2_DRIVER_BULKLOAD_BATCH_SIZE

    if args['datasvc_load']:
        if load_mode == constants.CH2_DRIVER_LOAD_MODE["NOT_SET"]:
            load_mode = constants.CH2_DRIVER_LOAD_MODE["DATASVC_LOAD"]
        else:
            logging.info("Cannot specify multiple types of load")
            sys.exit(0)

    if args['datasvc_bulkload'] or args['datasvc_load']:
        if args['kv_timeout']:
            kv_timeout = args['kv_timeout']
        else:
            kv_timeout = constants.CH2_DRIVER_KV_TIMEOUT

    if args['qrysvc_load']:
        if load_mode == constants.CH2_DRIVER_LOAD_MODE["NOT_SET"]:
            load_mode = constants.CH2_DRIVER_LOAD_MODE["QRYSVC_LOAD"]
        else:
            logging.info("Cannot specify multiple types of load")
            sys.exit(0)
    if not args['no_load']:
       if load_mode == constants.CH2_DRIVER_LOAD_MODE["NOT_SET"]:
            logging.info("Need to specify the type of load")
            sys.exit(0)

    numTClients = args['tclients']
    numAClients = args['aclients']
    numClients = numTClients + numAClients
    duration = args['duration']
    queryIterations = args['query_iterations']
    warmupDuration = args['warmup_duration']
    warmupQueryIterations = args['warmup_query_iterations']
    if (numClients == 0):
        logging.info("No clients specified")
        sys.exit(0)

    if not args['no_execute']:
        if (duration == None and numAClients == 0):
            logging.info("Need a duration parameter for transaction clients to run")
            sys.exit(0)

    if not args['no_execute']:
        if (duration == None and queryIterations == None):
            logging.info("Need a duration or query-iterations parameter to run")
            sys.exit(0)

    if (duration != None and queryIterations != None):
        logging.info("Cannot specify both duration and query-iterations parameter to run")
        sys.exit(0)

    if ((duration != None and duration <= 0) or (queryIterations != None and queryIterations <= 0)):
        logging.info("Need a positive non-zero duration/query-iterations parameter to run")
        sys.exit(0)

    if ((warmupDuration != None and warmupDuration <= 0) or (warmupQueryIterations != None and warmupQueryIterations <= 0)):
        logging.info("Need a positive non-zero warmup duration/query-iterations parameter to run")
        sys.exit(0)

    if (warmupDuration != None and warmupQueryIterations != None):
        logging.info("Cannot specify both warmup duration and warmup query-iterations parameter to run")
        sys.exit(0)

    if (duration == None and warmupDuration != None):
        logging.info("Cannot specify warmup duration without specifying a total benchmark duration")
        sys.exit(0)

    if (queryIterations == None and warmupQueryIterations != None):
        logging.info("Cannot specify warmup query iterations without specifying number of total query iterations")
        sys.exit(0)

    if (duration != None and warmupDuration != None and duration < warmupDuration):
        logging.info("Total duration cannot be less than warmup duration!")
        sys.exit(0)

    if (queryIterations != None and warmupQueryIterations != None and queryIterations < warmupQueryIterations):
        logging.info("Total number of query iterations cannot be less than the number of warmup query iterations")
        sys.exit(0)

    if (warmupDuration == None and warmupQueryIterations == None):
        warmupDuration = 0
        warmupQueryIterations = 0

    ## Create a handle to the target client driver
    driverClass = createDriverClass(args['system'])
    assert driverClass != None, "Failed to find '%s' class" % args['system']
    val = -1
    if args['no_execute']:
         val = 0
         driver = driverClass(args['ddl'], val, "L", load_mode, kv_timeout, bulkload_batch_size)
    else:
        TAFlag = "T"
        if numClients == 1:
            if numAClients == 1:
                TAFlag = "A"
                val = 0
        driver = driverClass(args['ddl'], val, TAFlag)
    assert driver != None, "Failed to create '%s' driver" % args['system']
    if args['print_config']:
        config = driver.makeDefaultConfig()
        print (driver.formatConfig(config))
        print
        sys.exit(0)

    ## Load Configuration file
    if args['config']:
        logging.debug("Loading configuration file '%s'" % args['config'])
        cparser = SafeConfigParser()
        cparser.read(os.path.realpath(args['config'].name))
        config = dict(cparser.items(args['system']))
    else:
        logging.debug("Using default configuration for %s" % args['system'])
        defaultConfig = driver.makeDefaultConfig()
        config = dict(map(lambda x: (x, defaultConfig[x][1]), defaultConfig.keys()))
    config['reset'] = args['reset']
    config['load'] = False
    config['execute'] = False
    if config['reset']: logging.info("Reseting database")
    driver.loadConfig(config)
    logging.info("Initializing TPC-C benchmark using %s" % driver)

    ## Create ScaleParameters
    scaleParameters = scaleparameters.makeWithScaleFactor(args['warehouses'], args['scalefactor'])
    rand.setNURand(nurand.makeForLoad())
    if args['debug']: logging.debug("Scale Parameters:\n%s" % scaleParameters)

    ## DATA LOADER!!!
    numClients = numTClients + numAClients
    load_time = None
    if not args['no_load']:
        logging.info("Loading TPC-C benchmark data using %s" % (driver))
        load_start = time.time()
        if numClients == 1:
            l = loader.Loader(driver, scaleParameters, range(scaleParameters.starting_warehouse, scaleParameters.ending_warehouse+1), True)
            driver.loadStart()
            l.execute()
            driver.loadFinish()
        else:
            startLoading(driverClass, scaleParameters, args, config, load_mode, kv_timeout, bulkload_batch_size)
        load_time = time.time() - load_start
    ## IF

    ## WORKLOAD DRIVER!!!
    if not args['no_execute']:
        m = multiprocessing.Manager()
        qDone = m.Queue()
        warmupDurationQ = m.Queue()
        if numClients == 1:
            if numTClients == 1:
                TAFlag = "T"
            else:
                TAFlag = "A"
            e = executor.Executor(0, driver, qDone, warmupDurationQ, scaleParameters, TAFlag, warmupDuration, warmupQueryIterations, stop_on_error=args['stop_on_error'])
            driver.executeStart()
            results = e.execute(duration, queryIterations, warmupDuration, warmupQueryIterations, numAClients)
            driver.executeFinish()
        else:
            results = startExecution(driverClass, qDone, warmupDurationQ, warmupDuration, warmupQueryIterations, scaleParameters, args, config)
            print('Execution Completed')
        assert results
        print (results.show(duration, queryIterations, numClients, numAClients, load_time))
    ## IF

## MAIN
