
import io
import json
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def handler(ctx, data: io.BytesIO = None):
    """
    A simple diagnostic function to test VCN integration.
    If this function's logs are visible, it means the network environment
    was successfully prepared by the OCI Functions service.
    """
    logger.info("VCN Diagnostic Function started successfully.")
    
    # You can add a simple network check here if you want, like pinging
    # a known internal IP, but just getting this log message is proof enough.
    
    logger.info("Network environment appears to be configured.")
    
    return {
        "status": "success",
        "message": "VCN Diagnostic Function executed."
    }
