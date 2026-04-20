from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str

log = core.getLogger()

class NetworkMonitor(object):

    def __init__(self):
        core.openflow.addListeners(self)
        self.stats = {}

        core.callDelayed(5, self.request_stats)

    def request_stats(self):
        for connection in core.openflow._connections.values():
            connection.send(of.ofp_stats_request(
                body=of.ofp_flow_stats_request()
            ))
        core.callDelayed(5, self.request_stats)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        # FLOOD packets
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

        # INSTALL FLOW RULE
        match = of.ofp_match.from_packet(packet, in_port)

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = match
        flow_mod.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        flow_mod.idle_timeout = 10
        flow_mod.hard_timeout = 30

        event.connection.send(flow_mod)

    def _handle_FlowStatsReceived(self, event):
        dpid = dpid_to_str(event.connection.dpid)

        for flow in event.stats:
            key = (dpid, str(flow.match))
            byte_count = flow.byte_count

            if key in self.stats:
                old_bytes = self.stats[key]
                bandwidth = ((byte_count - old_bytes) * 8) / (5 * 1024 * 1024)

                log.info("Switch %s | Bandwidth: %.4f Mbps",
                         dpid, bandwidth)

            self.stats[key] = byte_count


def launch():
    core.registerNew(NetworkMonitor)
