# Sets up a local python venv, if required, then uses it to run the cli.py interface to mddocproc.
$VENV_NAME = 'venv'

if (!(Test-Path $VENV_NAME)) {
    . $PSScriptRoot\virtualenv.ps1
}

.\venv\scripts\mddocproc.exe $args

exit 0
