"""jobmarket — análisis de demanda del mercado laboral remoto."""

__version__ = "1.0.0"

from .classify import Job, classify, classify_all  # noqa: F401
from .normalize import find_terms, normalize  # noqa: F401

__all__ = ["Job", "classify", "classify_all", "normalize", "find_terms", "__version__"]
