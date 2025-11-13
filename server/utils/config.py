import os
from dotenv import load_dotenv

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"




CLAUDE_MODEL = "claude-3-opus-20240229"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
