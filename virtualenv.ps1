$REQUIRED_MAJOR_VERSION = 3
$REQUIRED_MINOR_MIN = 6
$REQUIRED_MINOR_MAX = 11
$BITNESS = "64"
$VENV_NAME = 'venv'

$versionToUse = ""
$pythonVersionsAvailable = py.exe --list

function FindPythonVersionToUse() {
    for ($i = $REQUIRED_MINOR_MAX; $i -ge $REQUIRED_MINOR_MIN; $i = $i - 1) {
        $major = $REQUIRED_MAJOR_VERSION
        $minor = $i
        $pythonVersion = "$major.$minor"
        foreach ($line in $pythonVersionsAvailable) {
            if ($line.Contains($pythonVersion) -AND $line.Contains($BITNESS)) {
                return "-$pythonVersion-$BITNESS"
            }
        }
    }
    return $null
}
Write-Host "##teamcity[progressMessage 'Finding an appropriate python version']"
$versionArgumentToUse = FindPythonVersionToUse
if ($versionArgumentToUse -eq $null) {
    Write-Host "##teamcity[progressMessage 'Failed to find an appropriate python version: 3.6 >= python <= 3.11']"
    exit -1
} else {
    Write-Host "##teamcity[progressMessage 'Using python version $versionArgumentToUse']"

    Write-Host "##teamcity[progressMessage 'Setting up virtualenv']"

    py $versionArgumentToUse -m pip install virtualenv
    py $versionArgumentToUse -m virtualenv $VENV_NAME
    $activate_command = '.\' + $VENV_NAME + '\Scripts\activate.ps1'
    Invoke-Expression $activate_command
    pip install -r $PSScriptRoot\requirements.txt --no-cache-dir
    python -m pip install pyinstaller
    exit 0
}
