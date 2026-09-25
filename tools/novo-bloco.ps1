<#
.SYNOPSIS
  Cria (ou completa) a pasta de um bloco em src/modules/<Nome> com o seu
  projeto Quartus de teste (.qpf/.qsf) e a pasta sim/ para o waveform.

.EXAMPLE
  .\tools\novo-bloco.ps1 somador4b
.EXAMPLE
  .\tools\novo-bloco.ps1 comp2 -Deps mux2x1,inversor
.EXAMPLE
  .\tools\novo-bloco.ps1 ula -Deps comp2,comparadores,aritmetica -Forcar

  -Deps   blocos usados DENTRO deste bloco. As dependencias das dependencias
          sao incluidas automaticamente (lidas do .qsf de cada uma).
  -Forcar regrava o .qsf se ele ja existir (use depois de mudar as Deps).
#>
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Nome,
    [string[]]$Deps = @(),
    [switch]$Forcar
)
$ErrorActionPreference = 'Stop'

$raiz    = Split-Path -Parent $PSScriptRoot
$modulos = Join-Path $raiz 'src/modules'
$dir     = Join-Path $modulos $Nome
$utf8    = New-Object System.Text.UTF8Encoding($false)

if ($Nome -cnotmatch '^[a-z][a-z0-9_]*$') {
    throw "Nome '$Nome' invalido: use snake_case minusculo (ex.: comparador_maior)."
}

New-Item -ItemType Directory -Force -Path (Join-Path $dir 'sim') | Out-Null

# Resolve dependencias transitivas lendo os SEARCH_PATH dos .qsf das deps
$todas = New-Object 'System.Collections.Generic.List[string]'
function Add-Dep([string]$d) {
    if ($todas.Contains($d) -or $d -eq $Nome) { return }
    $todas.Add($d)
    $q = Join-Path $modulos "$d/$d.qsf"
    if (-not (Test-Path $q)) {
        Write-Warning "Dependencia '$d' ainda nao tem projeto em src/modules/$d (crie-a antes, ou rode de novo com -Forcar depois)."
        return
    }
    foreach ($m in (Select-String -Path $q -Pattern 'SEARCH_PATH\s+\.\./(\S+)')) {
        Add-Dep $m.Matches[0].Groups[1].Value
    }
}
foreach ($d in $Deps) { foreach ($x in ($d -split ',')) { if ($x.Trim()) { Add-Dep $x.Trim() } } }

# .qpf
$qpf = Join-Path $dir "$Nome.qpf"
if (-not (Test-Path $qpf)) {
    [IO.File]::WriteAllText($qpf, "PROJECT_REVISION = `"$Nome`"`r`n", $utf8)
    Write-Host "  criado  src/modules/$Nome/$Nome.qpf"
}

# .qsf
$qsf = Join-Path $dir "$Nome.qsf"
if ((Test-Path $qsf) -and -not $Forcar) {
    Write-Host "  mantido src/modules/$Nome/$Nome.qsf (use -Forcar para regravar)"
} else {
    $l = @(
        "# Projeto de teste do bloco '$Nome' - gerado por tools/novo-bloco.ps1",
        '# Para mudar as dependencias, rode o script de novo com -Deps ... -Forcar',
        'set_global_assignment -name FAMILY "Cyclone IV E"',
        'set_global_assignment -name DEVICE EP4CE115F29C7',
        "set_global_assignment -name TOP_LEVEL_ENTITY $Nome",
        "set_global_assignment -name BDF_FILE $Nome.bdf",
        'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files'
    )
    foreach ($d in ($todas | Sort-Object)) { $l += "set_global_assignment -name SEARCH_PATH ../$d" }
    [IO.File]::WriteAllText($qsf, (($l -join "`r`n") + "`r`n"), $utf8)
    Write-Host "  gravado src/modules/$Nome/$Nome.qsf  (deps: $(if ($todas.Count) { $todas -join ', ' } else { 'nenhuma' }))"
}

$gk = Join-Path $dir '.gitkeep'
if (Test-Path $gk) { Remove-Item $gk }

if (-not (Test-Path (Join-Path $dir "$Nome.bdf"))) {
    Write-Host "  falta   src/modules/$Nome/$Nome.bdf (desenhe e salve com esse nome)"
}
