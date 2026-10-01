# Verificacao dos blocos da biblioteca (Quartus Prime, console Tcl: View > Utility Windows > Tcl Console)
#   source <repo>/ferramentas/verificacao/converter.tcl
# 1) converte cada lib/<bloco>.bdf em Verilog (saida/<bloco>.v), para simular com testa_blocos.py
# 2) roda Analysis & Synthesis em cada testes/<bloco> e grava o resumo em saida/log_map.txt
# Para analisar so alguns blocos: set only {ula comp_maior}; source .../converter.tcl
set here [file dirname [file normalize [info script]]]
set root [file normalize "$here/../.."]
set bin $quartus(binpath)
set out "$here/saida"
file delete -force $out
file mkdir $out
foreach f [glob "$root/lib/*.bdf"] { file copy -force $f $out }
set q [open "$out/conv.qpf" w]; puts $q "PROJECT_REVISION = \"conv\""; close $q
set q [open "$out/conv.qsf" w]
puts $q "set_global_assignment -name FAMILY \"Cyclone IV E\""
puts $q "set_global_assignment -name DEVICE EP4CE115F29C7"
close $q
cd $out
set log [open "$out/log_conv.txt" w]
foreach f [lsort [glob "$out/*.bdf"]] {
  set n [file tail $f]
  catch {exec "$bin/quartus_map" conv --convert_bdf_to_verilog=$n} res
  if {[regexp {was successful} $res]} { puts $log "OK   $n" } else { puts $log "ERRO $n\n$res" }
  file delete $f
}
close $log
set log [open "$out/log_map.txt" w]
foreach d [lsort [glob -type d "$root/testes/*"]] {
  set b [file tail $d]
  if {[info exists only] && [lsearch $only $b] < 0} continue
  cd $d
  catch {exec "$bin/quartus_map" --read_settings_files=on --write_settings_files=off $b -c $b} res
  if {[regexp {Analysis & Synthesis was successful} $res]} { puts $log "OK   $b" } else { puts $log "ERRO $b" }
  foreach l [split $res "\n"] { if {[regexp {^Error} $l]} { puts $log "     $l" } }
  flush $log
}
close $log
cd $root
puts "Fim: veja ferramentas/verificacao/saida/log_conv.txt e log_map.txt"
