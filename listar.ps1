function Show-Tree {
    param (
        [string]$Path = ".",
        [int]$Level = 0
    )

    $prefix = "|   " * $Level + "|-- "

    Get-ChildItem -LiteralPath $Path -Force | Where-Object {
        -not ($_.Name -in @('__pycache__', '.venv')) -and
        -not ($_.Name -like '*.pyc')
    } | Sort-Object { -not $_.PSIsContainer }, Name | ForEach-Object {
        Write-Output "$prefix$($_.Name)"
        if ($_.PSIsContainer) {
            Show-Tree -Path $_.FullName -Level ($Level + 1)
        }
    }
}

Show-Tree "." 0
