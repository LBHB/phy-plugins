# import from plugins/feature_view_custom_grid.py
"""Show how to customize the subplot grid specifiction in the feature view."""

import re
from phy import IPlugin, connect
from phy.cluster.views import AmplitudeView
import os.path as op
import numpy as np
from pdb import set_trace

def my_grid():
    """In the grid specification, 0 corresponds to the best channel, 1
    to the second best, and so on. A, B, C refer to the PC components."""
    s = """
    0A,1A 1A,2A 2A,0A
    0B,1B 1B,2B 2B,0B
    0C,1C 1C,2C 2C,0C
    """.strip()
    return [[_ for _ in re.split(' +', line.strip())] for line in s.splitlines()]


class BlockLines_on_Amplitude_Plugin(IPlugin):
    def attach_to_controller(self, controller):
        @connect
        def on_view_attached(view, gui):
            if isinstance(view, AmplitudeView):
                #set_trace()  
                blocksizes_path=op.join(controller.model.dir_path,'blocksizes.npy')
                if op.exists(blocksizes_path):
                    self.blocksizes=np.load(blocksizes_path)[0]
                    self.blockstarts=np.load(op.join(controller.model.dir_path,'blockstarts.npy'))[0]
                    self.blocksizes_time=self.blocksizes/controller.model.sample_rate
                    self.blockstarts_time=self.blockstarts/controller.model.sample_rate
                    self.gap=np.diff(self.blockstarts)-self.blocksizes[:-1]
                    self.gap_time=np.diff(self.blockstarts_time)-self.blocksizes_time[:-1]
                    self.show_block_gap=False
                    self.show_block_lines=True 
                else:
                    self.show_block_gap=False
                    self.show_block_lines=False
                    
                