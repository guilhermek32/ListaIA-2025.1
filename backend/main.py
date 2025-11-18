"""Main application entry point."""

import logging
from typing import Optional

import dspy
import pandas as pd
import numpy as np

from config import LOG_LEVEL, OPENAI_API_KEY
from dspy_modules import ChainOfThought, configure_lm
from utils import calculate_statistics

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_example():
    """Run a basic example using all libraries."""
    logger.info("Starting example application")
    
    # Example with numpy
    data = np.random.randn(100)
    stats = calculate_statistics(data)
    logger.info(f"Data statistics: {stats}")
    
    # Example with pandas
    df = pd.DataFrame({
        "A": np.random.randn(10),
        "B": np.random.randn(10),
        "C": np.random.randn(10),
    })
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"DataFrame head:\n{df.head()}")
    
    # Example with dspy (requires API key)
    if OPENAI_API_KEY:
        try:
            configure_lm(api_key=OPENAI_API_KEY)
            cot = ChainOfThought()
            response = cot(question="What is the capital of France?")
            logger.info(f"DSPy response: {response.answer}")
        except Exception as e:
            logger.error(f"DSPy example failed: {e}")
    else:
        logger.warning("OPENAI_API_KEY not set, skipping DSPy example")
    
    logger.info("Example completed")


if __name__ == "__main__":
    run_example()
