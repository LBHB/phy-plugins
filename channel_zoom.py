"""
Add channel zoom snippet (:cz) to TraceView
"""

from phy import IPlugin, connect
from phy.cluster.views import TraceView

class channel_zoom(IPlugin):
    def attach_to_controller(self, controller):
        @connect
        def on_view_attached(view, gui):
            if isinstance(view, TraceView):
                @gui.view_actions.add(alias='cz')  # corresponds to `:cz` snippet
                def channel_zoom(channel=None,N=6,view=view,controller=controller):
                        """Zoom over best channel."""
                        if channel is None:
                            cluster_ids = controller.supervisor.selected
                            channel=controller.get_best_channel(cluster_ids[0])
                        zo = [1, view.n_channels/N]
                        p  = [0, -2*channel/view.n_channels+1]
                        print(p)
                        view.canvas.panzoom.set_pan_zoom(zoom=zo,pan=p)
                        
