# config/telemetry.py

import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from config.env_loader import AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING

def init_telemetry():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Set log level globally

    # Silence some loggers
        # Silence azure.core.pipeline INFO-level logs
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
    logging.getLogger("azure.monitor.opentelemetry.exporter.export._base").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show INFO+ logs in the terminal
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    
    # Add the console handler to the root logger (only if not already added)
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)

    # Now we have a named logger for this module
    logger = logging.getLogger(__name__)

    if not AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING:
        logger.warning("Warning: No Application Insights connection string found.")
        return

    # Initialize Azure Monitor (captures logs, traces, metrics automatically)
    configure_azure_monitor(connection_string=AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING)

    logger.info("Azure Application Insights telemetry (including logs) initialized.")
