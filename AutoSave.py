"""AutoSave plugin.

To activate the plugin, copy this file to `~/.phy/plugins/` and add this line
to your `~/.phy/phy_config.py`:

```python
c.TemplateGUI.plugins = ['AutoSave']
```

Luke Shaheen - Laboratory of Brain, Hearing and Behavior Sept 2021
"""

import numpy as np
from phy import IPlugin, connect
import os.path as op
import threading
import time
# spike_clusters, groups, labels,
class AutoSave(IPlugin):

    def attach_to_controller(self, controller):
        @connect
        def on_gui_ready(sender,gui):

            #class BackgroundTimer(threading.Thread):
            #    def run(self):
            #        while 1:
            #            time.sleep(60*5)
            #            print('\Saving')
            #            print(time.localtime())
            #            gui.file_actions.save()

            #gui.timer = BackgroundTimer()
            #gui.timer.start()
            #print('Started timer')

            @connect(sender=controller.supervisor)
            def on_cluster(sender, up, gui=gui):
                """This is called every time a cluster assignment or cluster group/label
                changes."""
                print("Save on clustering")
                if up.description == 'metadata_group':
                    gui.file_actions.save()


        #@connect(sender=gui)
        #def on_close(sender):
        #    print('Stopped timer')
        #    sender.timer.stop()
