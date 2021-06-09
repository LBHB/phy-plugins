# import from plugins/n_spikes_views.py
"""Show how to change the number of displayed spikes in each view."""

from phy import IPlugin


class n_spikes_per_view(IPlugin):
    def attach_to_controller(self, controller):
        """Feel free to keep below just the values you need to change."""
        controller.n_spikes_waveforms = 300 #deault 100. Number of spikes per cluster in WaveformView
        #controller.batch_size_waveforms = 10
        #controller.n_spikes_features = 10000
        #controller.n_spikes_features_background = 2500
        controller.n_spikes_amplitudes = 20000 #deault 10000. Number of spikes per cluster in AmplitudeView
        #controller.n_spikes_correlograms = 100000

        # Number of "best" channels kept for displaying the waveforms.
        #controller.model.n_closest_channels = 12

        # The best channels are selected among the N closest to the best (peak) channel if their
        # mean amplitude is greater than this fraction of the peak amplitude on the best channel.
        # If zero, just the N closest channels are kept as the best channels.
        #controller.model.amplitude_threshold = 0
