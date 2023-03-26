$FAILURE=1
$SUCCESS=0

function CreateStartupApp($Name, $RunPath) {
    Write-Host "[Win10] Creating startup app '$Name' -> $RunPath"

    $RegItem = @{
        Path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
        Name = $Name
    }

    # Create path if missing
    $Path = Get-Item -Path $RegItem.Path -ErrorAction SilentlyContinue
    if ($null -eq $Path) { New-Item -Path $RegItem.Path }

    if ($null -eq (Get-ItemProperty @RegItem -ErrorAction SilentlyContinue)) {
        New-ItemProperty @RegItem -Value "$RunPath" -PropertyType DWord -Force | Out-Null
        Write-Host 'Added Registry value' -f Green
    } else {
        Write-Host "Value already exists" -f Yellow
        #set-ItemProperty @RegItem -Value "$RunPath"
    }
}

$request=$args[0]

Switch ($request)
{
    {$_ -match 'test'} {
        Write-Host "---=== TEST CLAUSE OR PLACEHOLDER ===---"
        Write-Host "  Will not actually install anything."
        Write-Host " "
        Write-Host -NoNewLine 'Press any key to continue...';
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
        Exit $SUCCESS
    }
    {$_ -match 'startup'} {
        $prog_name=$args[1]
        $prog_path=$args[2]
        CreateStartupApp "$prog_name" "$prog_path"
        Exit $SUCCESS
    }
    default {
        Write-Host "Request invalid"
        Exit $FAILURE
    }
}
