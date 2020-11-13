#!/usr/bin/python3

import logger
import trace_train
from conf_gt import ConfGetTrain
import conf

def __usage_getrain():
    print("""\
Usage: getrain.py [<options>] <path>
  <options>
   -o <output>
   -d <dim>: bitmap dimension, format: widthxheight
   -i <interval>: timestamp interval for width
   -M <lba max>
   -B <block range>
   -T <timestamp range>
   -R: analyze only read access
   -W: analyze only write access
   -P <pid>: analyze accesses with given pid
   -f <count>: forward columns (default: 1)
   -H: human readable output(no csv)
""")

class GetTrain:
    def getdata(self):
        for path in conf.paths:
            tt = trace_train.TraceTrain()
            if not tt.load(path):
                return
            tt.gen_train_data()

if __name__ == "__main__":
    import getrain

    logger.init("getrain")

    gt = getrain.GetTrain()
    ConfGetTrain(__usage_getrain)
    exit(gt.getdata())
