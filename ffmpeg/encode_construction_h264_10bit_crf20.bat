@ECHO OFF

SET FFMPEG_BIN=D:\tools\ffmpeg-20151027-git-e6f9952-win64-static-x264-10bit\bin\ffmpeg.exe

IF NOT EXIST %FFMPEG_BIN% (
  ECHO ffmpeg executable not found
  PAUSE
  EXIT
)

SET /p INFILE=Input file: 

SET COMMAND=%FFMPEG_BIN% -i "%INFILE%" -r 59.94 -vf "yadif=1:-1:0" -c:v libx264 -crf 20 -pix_fmt yuv420p10le -profile:v high10 -level 5 -tune film -preset veryslow -an -sn -y "%INFILE%.mkv"

ECHO EXECUTUNG %COMMAND%
%COMMAND%
PAUSE

:: x264opt
::  cabac=1
::  ref=16
::  deblock=1:-1:-1
::  analyse=0x3:0x133
::  me=umh
::  subme=10
::  psy=1
::  psy_rd=1.00:0.15
::  mixed-ref=1
::  me_range=24
::  chroma_me=1
::  trellis=2
::  8x8dct=1
::  cqm=0
::  deadzone=21,11
::  fast_pskip=1
::  chroma_qp_offset=-3
::  nr=0
::  decimate=1
::  interlaced=0
::  bluray_compat=0
::  constrained_intra=0
::  bframes=8
::  b_pyramid=2
::  b_adapt=2
::  b_bias=0
::  direct=3
::  weightdb=1
::  open_gop=0
::  weightp=2
::  keyint=250
::  keyint_min=25
::  scenecut=40
::  intra_refresh=0
::  rc_lookahead=60
::  rc=crf
::  mbtree=1
::  crf=20.0
::  qcomp=0.60
::  qpmin=0
::  qpmax=81
::  qpstep=4
::  ip_ratio=1.40
::  aq=1:1.00
