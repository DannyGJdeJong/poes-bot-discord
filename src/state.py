from collections import defaultdict
from chatgpt import ChatGPTMessage
import constants

memory: defaultdict[str, list[ChatGPTMessage]] = defaultdict(list)
context: defaultdict[str, str] = defaultdict(lambda: constants.DEFAULT_CONTEXT)
