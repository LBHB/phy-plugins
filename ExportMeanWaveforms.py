"""ExportMeanWaveforms output plugin.
This plugin creates a npy file containing an array of the mean waveform for
each cluster (N_channels,N_samples,N_clusters)
This plugin is called a s ansippet. To use it type ':' to get into snippet mode,
then type:
emw
or
emw N
where N is the max number of waveforms per cluster to use to create the mean waveform (default 1000)
use a really high number to use all waveforms.
To activate the plugin, copy this file to `~/.phy/plugins/` and add this line
to your `~/.phy/phy_config.py`:
```python
c.TemplateGUI.plugins = ['ExportMeanWaveforms']
```
Luke Shaheen - Laboratory of Brain, Hearing and Behavior Nov 2016
"""

import numpy as np
from phy import IPlugin, connect
import os.path as op
from PyQt5.QtWidgets import QMessageBox

def export_mean_waveforms(max_waveforms_per_cluster=1E4,controller=None):
    #make max_waveforms_per_cluster a really big number if you want to get all the waveforms (slow)
    #from PyQt5.QtCore import pyqtRemoveInputHook
    #pyqtRemoveInputHook()
    #import pdb; pdb.set_trace()
    cluster_ids = controller.supervisor.clustering.cluster_ids
    mean_waveforms = np.zeros((controller.model.n_samples_waveforms, len(cluster_ids)))
    for i, ci in enumerate(cluster_ids):
        print(f'Exporting mean waveform for cluster: {ci}, i={i+1}/{len(cluster_ids)} clusters')
        mw = controller._get_mean_waveforms(ci)
        best_chan = controller.get_best_channel(ci)
        bci = np.argwhere(mw.channel_ids==best_chan).squeeze()
        data = mw.data[0, :, bci]
        mean_waveforms[:, i] = data.squeeze() 
    np.save(op.join(controller.model.dir_path,'mean_waveforms.npy'),mean_waveforms)
    print('Done exporting mean waveforms')


class ExportMeanWaveforms(IPlugin):
    def attach_to_controller(self, controller):
        @connect
        def on_gui_ready(sender, gui):
            @connect(sender=gui)
            def on_request_save(sender, *args, controller=controller):
                msgBox = QMessageBox()
                msgBox.setText("Save mean waveforms?")
                msgBox.setInformativeText("Always do this on final save, but if sorting is still work in progress, might skip this step for speed")
                msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
                msgBox.setDefaultButton(QMessageBox.Save)
                ret = msgBox.exec()
                if ret == QMessageBox.Save:
                    export_mean_waveforms(controller=controller)
                else:
                    pass
