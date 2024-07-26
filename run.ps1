param (
    [Parameter(Mandatory=$true)]
    [string]$Source,

    [Parameter(Mandatory=$true)]
    [string]$Target
)

$venvName = ".venv"
Set-Location $PSScriptRoot

if(-not (Test-Path -Path "./$venvName")){
    Write-Error "Could not find python virtual environment."
    Read-Host
    return
	
    # python -m venv $venvName
	# Ensure necessary packages are installed
	# & pip install -r ./requirements/requirements.txt
}

& "./$venvName/Scripts/Activate.ps1"

if(-not [bool]$env:VIRTUAL_ENV){
    Write-Error "Could not activate python virtual environment."
    Read-Host
    return
}

python -m main --source $Source --target $Target
