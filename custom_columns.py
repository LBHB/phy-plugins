"""Show how to customize the columns in the cluster and similarity views."""

from phy import IPlugin, connect


class custom_columns(IPlugin):
    def attach_to_controller(self, controller):
        @connect
        def on_controller_ready(sender):
            controller.supervisor.columns = ['id', 'ch',  'n_spikes', 'group','snr', 'fr', 'ContamPct','KSLabel']
