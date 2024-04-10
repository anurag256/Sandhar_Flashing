@echo off

set "tool_path=C:\Users\anura\Downloads\MRK3 2_Link\MRK3Link_EXE_V1.92\MRK3Link.exe"
set "device_index=0"
set "hex_file=C:\Users\anura\OneDrive\Documents\sketch_mar12a.ino.hex"

if not exist "%tool_path%" (
    echo Tool path not found.
    exit /b 1
)

REM Open the tool and select the device
"%tool_path%" --usb %device_index%

REM Execute the download command
"%tool_path%" --download EROM,"%hex_file%"
