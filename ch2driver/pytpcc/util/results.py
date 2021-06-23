# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http://www.cs.brown.edu/~pavlo/
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
import time
import constants

class Results:
    
    def __init__(self):
        self.start = None
        self.stop = None
        self.txn_id = 0
        
        self.txn_counters = { }
        self.txn_status = { }
        self.txn_times = { }
        self.running = { }
        self.query_times = []
        
    def startBenchmark(self):
        """Mark the benchmark as having been started"""
        assert self.start == None
        logging.debug("Starting benchmark statistics collection")
        self.start = time.time()
        return self.start
        
    def stopBenchmark(self):
        """Mark the benchmark as having been stopped"""
        assert self.start != None
        assert self.stop == None
        logging.debug("Stopping benchmark statistics collection")
        self.stop = time.time()
        
    def startTransaction(self, txn):
        self.txn_id += 1
        id = self.txn_id
        self.running[id] = (txn, time.time())
        return id
        
    def abortTransaction(self, id):
        """Abort a transaction and discard its times"""
        assert id in self.running
        txn_name, txn_start = self.running[id]
        del self.running[id]

        if txn_name not in self.txn_status :
             self.txn_status[txn_name] = {}

        status = "aborted"
        cnt = self.txn_status[txn_name].get(status, 0)
        self.txn_status[txn_name][status] = cnt + 1
        
    def stopTransaction(self, id, status):
        """Record that the benchmark completed an invocation of the given transaction"""
        assert id in self.running
        txn_name, txn_start = self.running[id]
        del self.running[id]
        
        duration = time.time() - txn_start
        total_time = self.txn_times.get(txn_name, 0)
        self.txn_times[txn_name] = total_time + duration

        total_cnt = self.txn_counters.get(txn_name, 0)
        self.txn_counters[txn_name] = total_cnt + 1

        if txn_name not in self.txn_status :
             self.txn_status[txn_name] = {}

        if status != "":
            cnt = self.txn_status[txn_name].get(status, 0)
            self.txn_status[txn_name][status] = cnt + 1

    def append(self, r):
        for txn_name in r.txn_counters.keys():
            orig_cnt = self.txn_counters.get(txn_name, 0)
            orig_time = self.txn_times.get(txn_name, 0)

            self.txn_counters[txn_name] = orig_cnt + r.txn_counters[txn_name]
            self.txn_times[txn_name] = orig_time + r.txn_times[txn_name]
            logging.debug("%s [cnt=%d, time=%d]" % (txn_name, self.txn_counters[txn_name], self.txn_times[txn_name]))
        for txn_name in r.txn_status.keys():
             if txn_name not in self.txn_status :
                  self.txn_status[txn_name] = {}
             for k in r.txn_status[txn_name].keys():
                 cnt = self.txn_status[txn_name].get(k, 0)
                 self.txn_status[txn_name][k] = cnt + r.txn_status[txn_name][k]

        if len(r.query_times) > 0:
            self.query_times.append(r.query_times)
        ## HACK
        self.start = r.start
        if len(r.query_times) == 0:
            self.stop = r.stop
            
    def __str__(self):
        return self.show()
        
    def show(self, duration, queryIterations, numClients, numAClients, load_time = None):
        if self.start == None:
            return "Benchmark not started"
        if duration == None:
            if self.stop == None:
                res_duration = time.time() - self.start
            else:
                res_duration = self.stop - self.start
        else:
            res_duration = duration

        col_width = 15
        total_width = (col_width*5)
        f = "\n  " + (("%-" + str(col_width) + "s")*4)
        line = "-"*total_width

        ret = u"" + "="*total_width + "\n"
        if load_time != None:
            ret += "Data Loading Time: %d seconds\n\n" % (load_time)

        if duration != None:
            if duration == 1:
                ret += "\n\n\nTransaction Execution Results after %d second\n%s" % (duration, line)
            else:
                ret += "\n\n\nTransaction Execution Results after %d seconds\n%s" % (duration, line)
        else:
            if queryIterations == 1:
                ret += "\n\n\nTransaction Execution Results after %d query iteration\n%s" % (queryIterations, line)
            else:
                ret += "\n\n\nTransaction Execution Results after %d query iterations\n%s" % (queryIterations, line)
        ret += f % ("", "Executed", u"Time (µs)", "Rate")
        total_txn_time = 0
        total_txn_cnt = 0
        for txn in sorted(self.txn_counters.keys()):
            if txn == constants.QueryTypes.CH2:
                continue
            txn_time = self.txn_times[txn]
            txn_cnt = self.txn_counters[txn]
            txn_rate = u"%.02f txn/s" % ((txn_cnt / res_duration))
            #avg_latency = u"%.03f sec" % ((txn_cnt / txn_time))
            ret += f % (txn, str(txn_cnt), str(round(txn_time * 1000000,3)), txn_rate)
            total_txn_time += txn_time
            total_txn_cnt += txn_cnt
            ret += "("
            i = 0
            for k in sorted(self.txn_status[txn].keys()):
                if txn == constants.QueryTypes.CH2:
                    continue
                if i != 0 :
                   ret += ", "
                i += 1
                ret += k + ":"+ str(self.txn_status[txn][k])
            ret += ")"
        ret += "\n" + ("-"*total_width)
        total_rate = "%.02f txn/s" % ((total_txn_cnt / res_duration))
        ret += f % ("TOTAL", str(total_txn_cnt), str(round(total_txn_time * 1000000,3)), total_rate)


        col_width = 13
        total_width = (col_width*6)+5
        f = "\n  " + (("%-" + str(col_width) + "s")*6)
        line = "-"*total_width
        if duration != None:
            if duration == 1:
                ret += "\n\n\nAnalytics Execution Results after %d second\n%s" % (duration, line)
            else:
                ret += "\n\n\nAnalytics Execution Results after %d seconds\n%s" % (duration, line)
        else:
            if queryIterations == 1:
                ret += "\n\n\nAnalytics Execution Results after %d query iteration\n%s" % (queryIterations, line)
            else:
                ret += "\n\n\nAnalytics Execution Results after %d query iterations\n%s" % (queryIterations, line)
        total_analytics_time = 0
        total_analytics_cnt = 0
        overall_avg_resp_time = {"Q01": [0, 0], "Q02": [0, 0], "Q03": [0, 0], "Q04": [0, 0], "Q05": [0, 0], "Q06": [0, 0],
                                 "Q07": [0, 0], "Q08": [0, 0], "Q09": [0, 0], "Q10": [0, 0], "Q11": [0, 0], "Q12": [0, 0],
                                 "Q13": [0, 0], "Q14": [0, 0], "Q15": [0, 0], "Q16": [0, 0], "Q17": [0, 0], "Q18": [0, 0],
                                 "Q19": [0, 0], "Q20": [0, 0], "Q21": [0, 0], "Q22": [0, 0]}

        #HACK
        if numClients == 1:
            # Make self.query_times an array of arrays to keep the show() code consistent
            tmp = []
            tmp.append(self.query_times)
            self.query_times = tmp

#        print(self.query_times) #self.query_times is an array of arrays, one element for each client

        for qry_times in self.query_times: #qry_times is an array element, each element corresponds to one client
            ret += f % ("Client", "Query", "Loop", "Start Time", "End Time", u"Elapsed Time (s)")
            partialLoop = False
            for qry_dict in qry_times: # each dict corresponds to one loop of query execution
                geo_mean = 1
                total_time = 0
                numQueriesPerIteration = len(qry_dict)
                if numQueriesPerIteration < constants.NUM_CH2_QUERIES:
                    partialLoop = True
                    logging.debug("Partial Loop")

                for qry in qry_dict: # individual query
                    if qry_dict[qry][3][-2:] == "ms":
                        q_time = float(qry_dict[qry][3][:-2])/1000
                    elif qry_dict[qry][3][-1:] == "s":
                        q_time = float(qry_dict[qry][3][:-1])
                    if not partialLoop:
                        overall_avg_resp_time[qry][0] += round(q_time, 2)
                        overall_avg_resp_time[qry][1] += 1
                    ret += f % (qry_dict[qry][0], qry, qry_dict[qry][1], qry_dict[qry][2], qry_dict[qry][4], round(q_time, 2))
                    geo_mean *= q_time
                    total_time += q_time

                ret += "\n" + ("-"*total_width)
                if numQueriesPerIteration == 0:
                    ret += "\n" + ("QUERIES RUN = %d" %(numQueriesPerIteration))
                else:
                    ret += "\n" + ("QUERIES RUN = %d TOTAL TIME = %.02f GEOMETRIC MEAN = %.02f  ARITHMETIC MEAN = %.02f" %(numQueriesPerIteration, round(total_time, 2), round(geo_mean**(1./numQueriesPerIteration), 2), round(total_time/numQueriesPerIteration, 2)))
                
                ret += "\n"
                ret += "\n"

        if len(self.query_times) == 0:
            return(ret)
        
        overall_geo_mean = 1
        overall_num_queries = 0
        sum_avg_resp_time = 0
        for query in overall_avg_resp_time:
            if overall_avg_resp_time[query][1] > 0:
                overall_num_queries += 1
                overall_avg_resp_time[query][0] /= overall_avg_resp_time[query][1]
                overall_geo_mean *= overall_avg_resp_time[query][0]
                sum_avg_resp_time += overall_avg_resp_time[query][0]

        if sum_avg_resp_time == 0:
            return(ret)
        
        #print (overall_avg_resp_time)
        col_width = 25
        total_width = (col_width*2)+2
        f = "\n  " + (("%-" + str(col_width) + "s")*2)
        line = "-"*total_width
        ret += "\n" + ("OVERALL RESULTS FOR COMPLETED QUERY SETS")
        ret += "\n" + ("-"*total_width)
        ret += f % ("Query", u"Average Response Time (s)")
        ret += "\n" + ("-"*total_width)
        for query in overall_avg_resp_time:
            if overall_avg_resp_time[query][1] > 0:
                ret += f % (query, round(overall_avg_resp_time[query][0], 2))
        ret += "\n" + ("-"*total_width)
        ret += "\n" + ("OVERALL GEOMETRIC MEAN = %.02f" %(round(overall_geo_mean**(1./overall_num_queries), 2)))
        ret += "\n" + ("AVERAGE TIME PER QUERY SET = %.02f" %(round(sum_avg_resp_time, 2)))
        ret += "\n" + ("QUERIES PER HOUR (Qph) = %.02f" %(round(overall_num_queries * 3600/sum_avg_resp_time*numAClients, 2)))
        
        ret += "\n" + ("-"*total_width)
        return (ret)
## CLASS
