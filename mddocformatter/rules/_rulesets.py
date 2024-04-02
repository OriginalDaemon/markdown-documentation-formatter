from __future__ import annotations

from ._base import DocumentRule
from .._consts import DeploymentStyle
from . import (
    santize_internal_links,
    move_to_target_dir_relative,
    create_table_of_contents,
    apply_macros,
    rename_uniquely_for_confluence,
    add_glossary_links,
)

from typing import List, Dict


def GetRulesForStyle(style: DeploymentStyle) -> List[DocumentRule]:
    """
    Get the rule set to use for a given deployment style.
    """
    StandardRulesTable: Dict[DeploymentStyle, List[DocumentRule]] = {
        DeploymentStyle.GITHUB: [
            santize_internal_links,
            move_to_target_dir_relative,
        ],
        DeploymentStyle.CONFLUENCE: [
            create_table_of_contents,
            apply_macros,
            santize_internal_links,
            rename_uniquely_for_confluence,
            add_glossary_links,
        ],
        DeploymentStyle.CUSTOM: [],
    }
    return list(StandardRulesTable[style])
