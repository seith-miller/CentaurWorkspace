import warnings
from pydantic import PydanticDeprecatedSince20

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

# Suppress DeprecationWarning for google upb message container
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*_upb._message.*"
)

# Suppress DeprecationWarning for datetime.utcnow in posthog
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*datetime.utcnow.*"
)

# Suppress all other deprecation warnings as a catch-all
warnings.filterwarnings("ignore", category=DeprecationWarning)
