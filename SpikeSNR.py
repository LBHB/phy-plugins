"""SpikeSNR metric plugin.

This plugin adds a column to the metrics showing the spike SNR.

To activate the plugin, copy this file to `~/.phy/plugins/` and add this line
to your `~/.phy/phy_config.py`:

```python
c.TemplateGUI.plugins = ['SpikeSNR']
```

Luke Shaheen - Laboratory of Brain, Hearing and Behavior Dec 2016
adapted from custom_stats.py example
"""

from phy import IPlugin
import numpy as np

class SpikeSNR(IPlugin):
    def attach_to_controller(self, controller):
        def snr(cluster_id):
                # This function takes a cluster id as input and returns a scalar.
                # data.data is a (n_spikes, n_samples, n_channels) array.
                data = controller._get_waveforms(cluster_id)
    
                #(n_spikes, n_samples, n_channels)
                #m=data.data.max()
                #m=abs(data.data.min())
                noise_std=np.concatenate((data.data[:,:10,:],data.data[:,:10,:]),axis=1).std(axis=(0,1))
                sig_std=data.data.mean(0).std(0)
                m=(sig_std/noise_std).max()           # max snr across channels
                #m=erf(sig_std/noise_std/2).max()*100   # max "isolation" across channels
                #m=abs(data.data.mean(0).min()) # mean over selected spikes, min over all samples and channels
                print('Cluster {:d} has shape {}, snr is {:.2f}'.format(cluster_id,data.data.shape,m))
                return m
        # Use this dictionary to define custom cluster metrics.
        # We memcache the function so that cluster metrics are only computed once and saved
        # within the session, and also between sessions (the memcached values are also saved
        # on disk).
        controller.cluster_metrics['snr'] = controller.context.memcache(snr)
                            
                