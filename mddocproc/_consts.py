from enum import Enum


class DeploymentStyle(Enum):
    """
    A set of standard "styles" which are used to configure common sets of rule_set.
    """
    GITHUB = "github"
    CONFLUENCE = "confluence"


class Passes(Enum):
    """
    List of indices for the passes to run in the documentation processing step.
    """
    FIRST = 0
    LINK_UPDATING = 1
    FINALIZE = 2
