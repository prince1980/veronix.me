$ffmpeg = Resolve-Path .\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe
$ffprobe = Resolve-Path .\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe
$targetBytes = 99000000
$audioBitrate = 192000
$f = Get-Item 6.mp4
$duration = [double](& $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $f.FullName)
$factor = 0.98
$currentTotalBitrate = ($f.Length * 8.0) / $duration
$newTotalBitrate = $currentTotalBitrate * $factor
$videoBitrate = [int]($newTotalBitrate - $audioBitrate)
if ($videoBitrate -lt 500000) { $videoBitrate = 500000 }
$bufsize = [int]($videoBitrate * 2)
$logbase = Join-Path $env:TEMP ("ffmpeg2pass-" + $f.BaseName)
$out = Join-Path $f.DirectoryName ("{0}_adj.mp4" -f $f.BaseName)
Write-Host "Extra retune $($f.Name) vb=$videoBitrate"
& $ffmpeg -v quiet -stats -y -i $f.FullName -c:v libx264 -b:v $videoBitrate -minrate $videoBitrate -maxrate $videoBitrate -bufsize $bufsize -preset medium -x264-params "nal-hrd=cbr" -pass 1 -an -passlogfile $logbase -f mp4 NUL
& $ffmpeg -v quiet -stats -y -i $f.FullName -c:v libx264 -b:v $videoBitrate -minrate $videoBitrate -maxrate $videoBitrate -bufsize $bufsize -preset medium -x264-params "nal-hrd=cbr" -pass 2 -c:a aac -b:a $audioBitrate -movflags +faststart -passlogfile $logbase $out
Remove-Item $f.FullName; Rename-Item $out $f.FullName -Force
Remove-Item "$logbase*" -ErrorAction SilentlyContinue
