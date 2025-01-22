import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import connect_mt5, get_eurusd_data, detect_flag_pattern

logger = logging.getLogger(__name__)

class FlagConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        logger.info("WebSocket connection established.")
        await self.detect_flag_pattern()

    async def disconnect(self, close_code):
        self.running = False
        logger.info("WebSocket connection closed.")

    async def detect_flag_pattern(self):
        try:
            connect_mt5()
            while self.running:
                data = get_eurusd_data()
                logger.info(f"Retrieved EURUSD data: {data.shape[0]} rows")
                result = detect_flag_pattern(data)
                if result:
                    logger.info(f"Flag pattern detected: {result}")
                    await self.send_json({"flag_detected": True, "details": result})
                else:
                    logger.info("No flag pattern detected.")
                await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Error in detect_flag_pattern: {e}")
            await self.send_json({"flag_detected": False, "error": str(e)})