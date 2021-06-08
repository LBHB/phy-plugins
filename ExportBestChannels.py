"""ChannelExportUpdate output plugin.

This plugin adds to phy's default save function to additionally create
a best_channels.npy file containing the phy best channels when you press save.

To activate the plugin, copy this file to `~/.phy/plugins/` and add this line
to your `~/.phy/phy_config.py`:

```python
c.TemplateGUI.plugins = ['ExportBestChannels']
```

Luke Shaheen - Laboratory of Brain, Hearing and Behavior Nov 2016
"""

import numpy as np
from phy import IPlugin, connect
import os.path as op
# spike_clusters, groups, labels,
class ExportBestChannels(IPlugin):

    def attach_to_controller(self, controller):
        @connect
        def on_gui_ready(sender,gui):
            @connect
            def on_save_clustering(sender, spike_clusters, groups, *labels, controller=controller):
                cluster_ids = [key for key,value in groups.items() if value.lower() in ['good','mua']]
                best_channels = np.zeros(len(cluster_ids), dtype=int)
                best_channels_mapped = np.zeros(len(cluster_ids), dtype=int)
                for i in range(len(cluster_ids)):
                    best_channels[i]=controller.get_best_channel(cluster_ids[i])
                if hasattr(controller.model, 'channel_labels') and controller.model.channel_labels is not None:
                    best_channels=controller.model.channel_labels[best_channels]
                filename = controller.model.dir_path / 'best_channels.npy'
                np.save(filename,best_channels)
