$ScriptPath = Split-Path $MyInvocation.InvocationName
& "$ScriptPath/venv/Scripts/activate.ps1"

$manage = "$ScriptPath\manage.py"
$shell = "shell"
$ipy = "ipython"
& python $manage $shell "-i" $ipy