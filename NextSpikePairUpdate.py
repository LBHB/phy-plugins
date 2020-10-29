"""NextSpikePairUpdate output plugin.

This plugin adds a shortcut to the trace view to skip through spike pairs
organized by ISI.

To activate the plugin, copy this file to `~/.phy/plugins/` and add this line
to your `~/.phy/phy_config.py`:

```python
c.TemplateGUI.plugins = ['NexpSpikePairUpdate']
```

Luke Shaheen - Laboratory of Brain, Hearing and Behavior Jan 2017
"""

import numpy as np
from phy import IPlugin, connect
from phy.gui import Actions
import logging 

logger = logging.getLogger(__name__)

class NextSpikePairUpdate(IPlugin):
        
    def attach_to_controller(self, controller):
        @connect
        def on_gui_ready(sender,gui):
            #actions = Actions(gui)            
            def go_to_spike_pair(increment):
#                from PyQt5.QtCore import pyqtRemoveInputHook
#                from pdb import set_trace
#                pyqtRemoveInputHook()
#                set_trace()
                max_num=1000
                tv = gui.get_view('TraceView')
                m = controller.model
                cluster_ids = controller.supervisor.selected
                if len(cluster_ids) == 0:
                    return
                elif len(cluster_ids) == 1:
                    is_self=True
                else:
                    is_self=False
                try:
                    do_compute = self.current_clusters != cluster_ids
                except:
                    do_compute=True
                if do_compute:
                    print('computing spike pairs...')
                    spc = controller.supervisor.clustering.spikes_per_cluster
                    spike_ids = spc[cluster_ids[0]]
                    spike_times1 = m.spike_times[spike_ids]              
                    if is_self:
                        diffs=np.diff(spike_times1)
                        self.max_num=np.min((np.prod(diffs.shape),max_num))
                        self.order=np.argsort(np.absolute(diffs),axis=None)[:self.max_num]  
                        self.times=(spike_times1[self.order]+spike_times1[self.order+1])/2
                        self.diffs=spike_times1[self.order] - spike_times1[self.order+1]
                    else:
                         spike_ids = spc[cluster_ids[1]]
                         spike_times2 = m.spike_times[spike_ids]
                         N=10000
                         maxdiff=.030
                         try_num=1
                         while try_num<5:
                             self.diffs=np.zeros(N)
                             self.times=np.zeros(N)
                             i=-1
                             start=0
                             for st1 in spike_times1:
                                  st2i = start
                                  while st2i<len(spike_times2) and i<N-1:
                                     df = st1 - spike_times2[st2i]
                                     if df >= maxdiff:
                                         start += 1
                                         st2i += 1
                                     elif df > -maxdiff:
                                         i += 1
                                         self.diffs[i]=df
                                         self.times[i]=st1
                                         st2i += 1
                                     else:
                                         break
                                  if i==N-1:
                                     maxdiff = maxdiff/2
                                     try_num +=1
                                     break
                             if i<N-1:
                                 break
                         self.times=self.times[:i]
                         self.diffs=self.diffs[:i]
                         self.max_num=np.min((np.prod(self.diffs.shape),max_num))
                         self.order=np.argsort(np.absolute(self.diffs),axis=None)[:self.max_num]
                         self.times=self.times[self.order] - self.diffs[self.order]/2
                         self.diffs=self.diffs[self.order]
                         #diffs=np.repeat(spike_times1[:,None],spike_times2.shape,axis=1)-np.repeat(spike_times2[:,None],spike_times1.shape,axis=1).T
                         #self.max_num=np.min((np.prod(diffs.shape),max_num))
                         #self.order=np.argsort(np.absolute(diffs),axis=None)[:self.max_num]  
                         #indexes = np.unravel_index(self.order,diffs.shape)
                         #self.times=(spike_times1[indexes[0]]+spike_times2[indexes[1]])/2
                        #self.diffs=spike_times1[indexes[0]] - spike_times2[indexes[1]]

                    self.current_index=0
                    self.current_clusters=cluster_ids
                    print('done')
                else:
                    self.current_index += increment
                if self.current_index == self.max_num:
                    self.current_index=0
                elif self.current_index < 0:
                    self.current_index=self.max_num-1
                tv.go_to(self.times[self.current_index])
                print('Moved to %ds (ISI=%0.1fms, index %d)' % (self.times[self.current_index],self.diffs[self.current_index]*1000, self.current_index) )
                
            @controller.supervisor.actions.add(shortcut='alt+ctrl+pgdown',menu='TraceView')
            def go_to_next_spike_pair():
                go_to_spike_pair(1)

            @controller.supervisor.actions.add(shortcut='alt+ctrl+pgup',menu='TraceView')
            def go_to_previous_spike_pair():
                go_to_spike_pair(-1)

