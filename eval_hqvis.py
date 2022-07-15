import argparse
import datetime
import json
import random
import time
from pathlib import Path

import numpy as np
import os
import math
import json
import sys

from pycocotools.ytvos import YTVOS
from pycocotools.ytvoseval import YTVOSeval

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def ytvos_eval(result_file, result_types, ytvos, get_boundary_out, max_dets=(100, 300, 1000)):
    
    ytvos = YTVOS(ytvos, get_boundary=get_boundary_out)
    assert isinstance(ytvos, YTVOS)

    if len(ytvos.anns) == 0:
        print("Annotations does not exist")
        return
    
    assert result_file.endswith('.json')
    ytvos_dets = ytvos.loadRes(result_file)

    vid_ids = ytvos.getVidIds()
    for res_type in result_types:
        iou_type = res_type
        ytvosEval = YTVOSeval(ytvos, ytvos_dets, iou_type)
        ytvosEval.params.vidIds = vid_ids
        if res_type == 'proposal':
            ytvosEval.params.useCats = 0
            ytvosEval.params.maxDets = list(max_dets)
        ytvosEval.evaluate()
        ytvosEval.accumulate()
        ytvosEval.summarize()

def main(args):
    result_file = args.save_path
    ytvos = 'ytvos'
    ytvos_eval(result_file, ['boundary'], 'ytvis/annotations/ytvis_hq-test-new.json', True, max_dets=(100, 300, 1000))
    ytvos_eval(result_file, ['segm'], 'ytvis/annotations/ytvis_hq-test-new.json', False, max_dets=(100, 300, 1000))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(' inference script')
    args = parser.parse_args()
    main(args)
