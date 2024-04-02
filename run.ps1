# Sets up a local python venv, if required, then uses it to run the cli.py interface to mddocformatter.
$VENV_NAME = 'venv'

if (!(Test-Path $VENV_NAME)) {
    . $PSScriptRoot\virtualenv.ps1
}

.\venv\scripts\mddocformatter.exe $args

exit 0
