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
def startLoading(driverClass, scaleParameters, args, config):
    logging.debug("Creating client pool with %d processes" % args['clients'])
    pool = multiprocessing.Pool(args['clients'])
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)
    
    # Split the warehouses into chunks
    w_ids = list(map(lambda x: [ ], range(args['clients'])))
    for w_id in range(scaleParameters.starting_warehouse, scaleParameters.ending_warehouse+1):
        idx = int(w_id % args['clients'])
        w_ids[idx].append(w_id)
    ## FOR

    loader_results = [ ]
    for i in range(args['clients']):
        r = pool.apply_async(loaderFunc, (i, driverClass, scaleParameters, args, config, w_ids[i], True))
        loader_results.append(r)
    ## FOR
    
    pool.close()
    logging.debug("Waiting for %d loaders to finish" % args['clients'])
    pool.join()
## DEF

## ==============================================
## loaderFunc
## ==============================================
def loaderFunc(clientId, driverClass, scaleParameters, args, config, w_ids, debug):
    driver = driverClass(args['ddl'], clientId)
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
def startExecution(driverClass, scaleParameters, args, config):
    logging.debug("Creating client pool with %d processes" % args['clients'])

    pool = multiprocessing.Pool(args['clients'])
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)
    
    worker_results = [ ]
    for i in range(args['clients']):
        #random_num = randint(1, 20)
        #time.sleep(round((random_num*0.1),2))
        print('')
        r = pool.apply_async(executorFunc, (i, driverClass, scaleParameters, args, config, debug,))

        worker_results.append(r)

    ## FOR

    pool.close()

    pool.join()
    
    total_results = results.Results()

    for asyncr in worker_results:
        asyncr.wait()
        r = asyncr.get()
        assert r != None, "No results object returned!"
        if type(r) == int and r == -1: sys.exit(1)
        total_results.append(r)
    ## FOR
    
    return (total_results)
## DEF

## ==============================================
## executorFunc
## ==============================================
def executorFunc(clientId, driverClass, scaleParameters, args, config, debug):
    driver = driverClass(args['ddl'], clientId)
    assert driver != None
    logging.debug("Starting client execution: %s" % driver)
    
    config['execute'] = True
    config['reset'] = False
    driver.loadConfig(config)

    e = executor.Executor(clientId, driver, scaleParameters, stop_on_error=args['stop_on_error'])
    driver.executeStart()
    results = e.execute(args['duration'])
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
                         help='query-url <ip>:port', default = "127.0.0.1:9499")
    aparser.add_argument('--multi-query-url',
                         help = 'multi-query-url <ip>:port', default = "127.0.0.1:9499")
    aparser.add_argument('--config', type=argparse.FileType('r'),
                         help='Path to driver configuration file')
    aparser.add_argument('--reset', action='store_true',
                         help='Instruct the driver to reset the contents of the database')
    aparser.add_argument('--scalefactor', default=1, type=float, metavar='SF',
                         help='Benchmark scale factor')
    aparser.add_argument('--warehouses', default=4, type=int, metavar='W',
                         help='Number of Warehouses')
    aparser.add_argument('--duration', default=60, type=int, metavar='D',
                         help='How long to run the benchmark in seconds')
    aparser.add_argument('--ddl', default=os.path.realpath(os.path.join(os.path.dirname(__file__), "tpcc.sql")),
                         help='Path to the TPC-C DDL SQL file')
    aparser.add_argument('--clients', default=1, type=int, metavar='N',
                         help='The number of blocking clients to fork')
    aparser.add_argument('--stop-on-error', action='store_true',
                         help='Stop the transaction execution when the driver throws an exception.')
    aparser.add_argument('--no-load', action='store_true',
                         help='Disable loading the data')
    aparser.add_argument('--no-execute', action='store_true',
                         help='Disable executing the workload')
    aparser.add_argument('--print-config', action='store_true',
                         help='Print out the default configuration file for the system and exit')
    aparser.add_argument('--debug', action='store_true',
                         help='Enable debug log messages')
    aparser.add_argument('--durability_level',
                         help='durability level', default="majority")
    aparser.add_argument('--txtimeout', metavar='N', type=float, default=3,
                         help='txtimeout number in sec(ex: 2.5)')
    aparser.add_argument('--scan_consistency', metavar='not_bounded', default="not_bounded",
                         help='not_bounded,request_plus')
    aparser.add_argument('--run_date',
                         help='run date for TPCC data', default = "2021-01-01 00:00:00")
    args = vars(aparser.parse_args())
    print (args)
    if args['debug']: logging.getLogger().setLevel(logging.DEBUG)
    query_url = "127.0.0.1:9499"
    userid = "Administrator"
    password = "password"
    multi_query_url = "127.0.0.1:9499"
    if args['query_url']:
        query_url = args['query_url']
    os.environ["QUERY_URL"] = query_url
    if args['multi_query_url']:
        multi_query_url = args['multi_query_url']
        os.environ["MULTI_QUERY_URL"] = multi_query_url
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

    ## Create a handle to the target client driver
    driverClass = createDriverClass(args['system'])
    assert driverClass != None, "Failed to find '%s' class" % args['system']
    val = -1
    if args['no_execute']:
         val = 0
    driver = driverClass(args['ddl'], val)
    assert driver != None, "Failed to create '%s' driver" % args['system']
    if args['print_config']:
        config = driver.makeDefaultConfig()
        print (driver.formatConfig(config))
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
    load_time = None
    if not args['no_load']:
        logging.info("Loading TPC-C benchmark data using %s" % (driver))
        load_start = time.time()
        if args['clients'] == 1:
            l = loader.Loader(driver, scaleParameters, range(scaleParameters.starting_warehouse, scaleParameters.ending_warehouse+1), True)
            driver.loadStart()
            l.execute()
            driver.loadFinish()
        else:
            startLoading(driverClass, scaleParameters, args, config)
        load_time = time.time() - load_start
    ## IF
    
    ## WORKLOAD DRIVER!!!
    if not args['no_execute']:
        if args['clients'] == 1:
            e = executor.Executor(driver, scaleParameters, stop_on_error=args['stop_on_error'])
            driver.executeStart()
            results = e.execute(args['duration'])
            driver.executeFinish()
        else:
            results = startExecution(driverClass, scaleParameters, args, config)
            print('Execution Completed')
        assert results
        print (results.show(load_time))
    ## IF
    
## MAIN
