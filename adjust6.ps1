$ffmpeg = Resolve-Path .\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe
$audioBitrate = 192000
$f = Get-Item 6.mp4
$videoBitrate = 15000000
$bufsize = $videoBitrate * 2
$logbase = Join-Path $env:TEMP ("ffmpeg2pass-" + $f.BaseName)
$out = Join-Path $f.DirectoryName ("{0}_adj.mp4" -f $f.BaseName)
Write-Host "Force lower bitrate for $($f.Name)"
& $ffmpeg -v quiet -stats -y -i $f.FullName -c:v libx264 -b:v $videoBitrate -minrate $videoBitrate -maxrate $videoBitrate -bufsize $bufsize -preset medium -x264-params "nal-hrd=cbr" -pass 1 -an -passlogfile $logbase -f mp4 NUL
& $ffmpeg -v quiet -stats -y -i $f.FullName -c:v libx264 -b:v $videoBitrate -minrate $videoBitrate -maxrate $videoBitrate -bufsize $bufsize -preset medium -x264-params "nal-hrd=cbr" -pass 2 -c:a aac -b:a $audioBitrate -movflags +faststart -passlogfile $logbase $out
Remove-Item $f.FullName; Rename-Item $out $f.FullName -Force
Remove-Item "$logbase*" -ErrorAction SilentlyContinue
