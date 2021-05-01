@echo off

call conda activate o3

set CMD=%1

IF [%1]==[] goto USAGE

IF %CMD%==view goto VIEW
IF %CMD%==cycle goto CYCLE
IF %CMD%==layer goto LAYER 
IF %CMD%==cam goto CAM

IF %CMD%==mask goto MAKE_MASK
IF %CMD%==normal goto MAKE_NORMAL
IF %CMD%==d2p goto DEPTH_TO_POINTS
IF %CMD%==unpack-video goto UNPACK_VIDEO





:USAGE
echo ---------------------------------------------------------------------------
echo -                              p3 p3 p3                                   -
echo -                              p3      p3                                 -
echo -                              p3      p3                                 -
echo -                              p3 p3 p3                                   -
echo -                              p3                                         -
echo -                              p3                                         -
echo ---------------------------------------------------------------------------
echo "p3 capture                : capture snapshot of renderer frame"
echo "p3 view <*.png>           : render depth frame"
echo "p3 cam <obj>              : live camera depth with mesh, i.e p3 cam file.obj"
echo "p3 cycle <glob> <filepath>: cycle image(s) from source, i.e. p3 cycle *.png test.png"
echo ---------------------------------------------------------------------------
echo depth & video
echo ---------------------------------------------------------------------------
echo "p3 layer <png>       : draw/animate an image that is being continously overwritten"
echo "p3 mask <obj>   : make mask file from source object file
echo "p3 normal <obj> : make mask file from source object file
echo "p3 unpack-video <mp4>: extract frames from mp4 video
echo ---------------------------------------------------------------------------

goto END


:MAKE_MASK
python "%PC3_ROOT%/tools/remake_mask.py" %2
goto END

:MAKE_NORMAL
python "%PC3_ROOT%/tools/remake_normals.py" %2
goto END

:DEPTH_TO_POINTS
python %PC3_ROOT%/tools/src/d2p.py %2
goto END

:UNPACK_VIDEO/
python %PC3_ROOT%/tools/src/p3_vid2png.py %2
goto END


:CAM
pc3 *.png %2
goto END

:INIT
mkdir "c:/tmp/p3/%2"
goto END

:CD_CFG
set P3_WS=/tmp/p3/%2
cd %P3_WS%
echo %P3_WS%
echo 
goto END

:CTX
echo PC3_ROOT     : %PC3_ROOT%
echo P3_WORKSPACE : %P3_WS%
echo P3_MESHFILES : %P3_MESHFILE%
goto END

:VIEW
pc3 %2 %3
goto END

:LAYER
echo %2 %3 %4
p3loop.cmd %2 /tmp/config/default.json %INSTALL% %3
goto END

:CYCLE
python "%PC3_ROOT%/tools/src/imgcycle.py" %2 %3
goto END

:END


