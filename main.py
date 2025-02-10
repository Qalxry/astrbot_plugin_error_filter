import re
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.platform import AstrBotMessage
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.provider import LLMResponse
from astrbot.core.message.components import Plain
from openai.types.chat.chat_completion import ChatCompletion

@register("error_replacer", "Qalxry", "指定机器人的错误信息。", "1.0")
class ErrorFilter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.IsError_filter = self.config.get('IsError_filter', True)
        self.Error_reply = self.config.get('Error_reply', '')
    
    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        result = event.get_result()
        message_str = result.get_plain_text()
        if self.IsError_filter:
            if '请求失败' in message_str:
                logger.info(message_str)
                if self.Error_reply == '':
                    event.stop_event() # 停止回复
                result.chain.clear()
                result.message(self.Error_reply)
