from enum import Enum


class DeploymentStyle(Enum):
    GITHUB = "github"
    CONFLUENCE = "confluence"


class PASSES(Enum):
    """
    List of indices for the passes to run in the documentation processing step.
    """
    FIRST = 0
    LINK_UPDATING = 1
    FINALIZE = 2
