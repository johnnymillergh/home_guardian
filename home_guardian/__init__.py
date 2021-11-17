from home_guardian.configuration.application_configuration import (
    configure as application_configure,
)
from home_guardian.configuration.loguru_configuration import (
    configure as loguru_configure,
)
from home_guardian.configuration.thread_pool_configuration import (
    configure as thread_pool_configure,
)
from home_guardian.message.email import __init__

# Configuration
application_configure()
loguru_configure()
thread_pool_configure()

# Initialization
__init__()
