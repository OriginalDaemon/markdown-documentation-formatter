$VENV_NAME = 'venv'

if (!(Test-Path $VENV_NAME)) {
    . $PSScriptRoot\virtualenv.ps1
}

$activate_command = "$PSScriptRoot\$VENV_NAME\Scripts\activate.ps1"
Invoke-Expression $activate_command

python main.py $args

exit 0
