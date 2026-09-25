<#
.SYNOPSIS
  Migracao unica para a estrutura "um bloco por pasta" (src/modules/<bloco>/).
  Rode UMA vez, da raiz do repositorio, numa branch propria:

    git checkout develop; git pull origin develop
    git checkout -b chore/padroniza-estrutura
    powershell -ExecutionPolicy Bypass -File tools\padronizar.ps1

  O script so move/renomeia arquivos e cria os projetos de teste; ele NAO
  faz commit. Confira com "git status" antes de commitar.
#>
$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

if (-not (Test-Path '.git')) { throw 'Rode este script a partir do repositorio Projeto1SD.' }
if (Get-Process -Name quartus* -ErrorAction SilentlyContinue) {
    throw 'Feche o Quartus antes (ele trava os arquivos).'
}

function Rastreado([string]$p) {
    git ls-files --error-unmatch -- $p 2>$null | Out-Null
    return ($LASTEXITCODE -eq 0)
}
function Mover([string]$de, [string]$para) {
    if (-not (Test-Path $de)) { return }
    New-Item -ItemType Directory -Force -Path (Split-Path $para) | Out-Null
    if (Rastreado $de) { git mv -f -- $de $para } else { Move-Item -Force $de $para }
    Write-Host "  $de -> $para"
}
function Remover([string]$p) {
    if (-not (Test-Path $p)) { return }
    if (Rastreado $p) { git rm -q -- $p } else { Remove-Item -Force $p }
    Write-Host "  removido $p"
}

Write-Host '1) Um bloco por pasta'
Mover 'src/modules/ula/c2/dmux2x1.bdf'  'src/modules/mux2x1/mux2x1.bdf'
Mover 'src/modules/ula/c2/dmux2x1.bsf'  'src/modules/mux2x1/mux2x1.bsf'
Mover 'src/modules/ula/c2/inversor.bdf' 'src/modules/inversor/inversor.bdf'
Mover 'src/modules/ula/c2/inversor.bsf' 'src/modules/inversor/inversor.bsf'
Mover 'src/modules/ula/c2/comp2.bdf'    'src/modules/comp2/comp2.bdf'
Mover 'src/modules/ula/c2/comp2.bsf'    'src/modules/comp2/comp2.bsf'
Mover 'src/modules/comparadores/comparador_igual.bdf' 'src/modules/comparador_igual/comparador_igual.bdf'
Mover 'src/modules/comparadores/comparador_igual.bsf' 'src/modules/comparador_igual/comparador_igual.bsf'

Write-Host '2) Renomeia dmux2x1 -> mux2x1 (nome do simbolo nos .bdf/.bsf)'
$utf8 = New-Object System.Text.UTF8Encoding($false)
Get-ChildItem 'src/modules' -Recurse -Include *.bdf, *.bsf | ForEach-Object {
    $t = [IO.File]::ReadAllText($_.FullName)
    if ($t.Contains('"dmux2x1"')) {
        [IO.File]::WriteAllText($_.FullName, $t.Replace('"dmux2x1"', '"mux2x1"'), $utf8)
        Write-Host "  $($_.Name)"
    }
}

Write-Host '3) Waveforms locais (estavam em simulation/, que o .gitignore ignora)'
$vwfs = @{
    'comparador_igual' = @('simulation/waveform_comparador_igual.vwf')
    'inversor'         = @('simulation/waveform_inversor.vwf', 'src/modules/ula/c2/Waveform.vwf')
    'comp2'            = @('simulation/waveform_comp2.vwf', 'src/modules/ula/c2/Waveform1.vwf')
}
foreach ($bloco in $vwfs.Keys) {
    foreach ($orig in $vwfs[$bloco]) {
        $dest = "src/modules/$bloco/sim/$bloco.vwf"
        if ((Test-Path $orig) -and -not (Test-Path $dest)) { Mover $orig $dest }
    }
}

Write-Host '4) Remove pastas antigas vazias'
Remover 'src/modules/comparadores/.gitkeep'
Remover 'src/modules/display/.gitkeep'
Remover 'src/modules/ula/.gitkeep'
foreach ($d in 'src/modules/ula/c2', 'src/modules/ula', 'src/modules/comparadores', 'src/modules/display') {
    if ((Test-Path $d) -and -not (Get-ChildItem $d -Recurse -File)) { Remove-Item -Recurse -Force $d }
}

Write-Host '5) Projetos de teste de cada bloco'
$novo = Join-Path $PSScriptRoot 'novo-bloco.ps1'
& $novo mux2x1
& $novo inversor
& $novo comp2 -Deps mux2x1, inversor
& $novo comparador_igual

git add -A
Write-Host ''
Write-Host 'Pronto. Confira com "git status". Se sobrou algo em src/modules/ula ou'
Write-Host 'src/modules/comparadores (db/, output_files/...), pode apagar a pasta.'
