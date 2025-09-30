"""
Logging configuration for FlavorGraph backend
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with consistent formatting"""
    
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Create a default logger instance that can be imported directly
logger = setup_logger("flavorgraph")
