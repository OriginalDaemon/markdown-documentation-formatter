import _rules as rules
from ._processing import ProcessingSettings, ProcessingContext
from ._consts import DeploymentStyle
from ._utils import load_consts_from_py_file

from pathlib import Path
from typing import Dict



RulesTable = {
    DeploymentStyle.GITHUB: [
        rules.santize_internal_links,
        rules.move_to_target_dir_relative
    ],
    DeploymentStyle.CONFLUENCE: [
        rules.create_table_of_contents,
        rules.replace_variables,
        rules.santize_internal_links,
        rules.rename_uniquely_for_confluence
    ]
}


def ProcessDocs(
    inputDir: Path, outputDir: Path, deployment_style: DeploymentStyle, consts: Dict[str, str], version_name: str
):
    settings = ProcessingSettings(inputDir, outputDir, version_name, RulesTable[deployment_style], consts)
    context = ProcessingContext(settings)
    for totalDirs, dirProgress, currentDir, totalFiles, fileProgress, currentFile in walk_directories(inputDir):
        context.add_document(currentFile)
    context.run()
