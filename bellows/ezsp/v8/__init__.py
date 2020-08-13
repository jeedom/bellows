""""EZSP Protocol version 8 protocol handler."""
import logging
from typing import Tuple

import bellows.config
import voluptuous
from zigpy.typing import DeviceType

from . import commands, config, types as v8_types
from .. import protocol

EZSP_VERSION = 8
LOGGER = logging.getLogger(__name__)


class EZSPv8(protocol.ProtocolHandler):
    """EZSP Version 8 Protocol version handler."""

    COMMANDS = commands.COMMANDS
    SCHEMAS = {
        bellows.config.CONF_EZSP_CONFIG: voluptuous.Schema(config.EZSP_SCHEMA),
        bellows.config.CONF_EZSP_POLICIES: voluptuous.Schema(config.EZSP_POLICIES_SCH),
    }
    types = v8_types

    def _ezsp_frame_tx(self, name: str) -> bytes:
        """Serialize the frame id."""
        cmd_id = self.COMMANDS[name][0]
        hdr = [self._seq, 0x00, 0x01]
        return bytes(hdr) + self.types.uint16_t(cmd_id).serialize()

    def _ezsp_frame_rx(self, data: bytes) -> Tuple[int, int, bytes]:
        """Handler for received data frame."""
        seq, data = data[0], data[3:]
        frame_id, data = self.types.uint16_t.deserialize(data)

        return seq, frame_id, data

    async def set_source_route(self, device: DeviceType) -> v8_types.EmberStatus:
        """Set source route to the device if known."""
        return v8_types.EmberStatus.SUCCESS

    async def set_source_routing(self) -> None:
        """Enable source routing on NCP."""
        await self.setSourceRouteDiscoveryMode(1)
