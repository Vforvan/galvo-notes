@echo off
rem ============================================================
rem  五轴振镜 5D 补偿实验台 - 一键启动
rem  用法：双击本文件；或 启动网页.bat 8010 指定端口
rem ============================================================
setlocal EnableDelayedExpansion
title 五轴振镜 5D 补偿实验台

rem --- 定位脚本所在目录（双击时当前目录可能不是项目根目录）---
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
cd /d "%ROOT%"

rem --- 端口：默认 8000，可用第一个参数覆盖 ---
set "PORT=%~1"
if "%PORT%"=="" set "PORT=8000"
set "FIXED=0"
if not "%~1"=="" set "FIXED=1"

echo.
echo   五轴振镜 5D 补偿实验台
echo   项目目录：%ROOT%
echo   使用端口：%PORT%
echo.

rem ---------- 1. 检查虚拟环境 ----------
if not exist ".venv\Scripts\python.exe" (
    echo   [1/4] 未找到虚拟环境 .venv，开始自动创建...
    py -m venv .venv
    if errorlevel 1 (
        echo.
        echo   [错误] 创建虚拟环境失败。
        echo   请确认已安装 Python 3.10 或更高版本，且 "py" 命令可用。
        echo   下载地址：https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
    echo         正在安装依赖，首次可能需要几分钟...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -e ".[dev]"
    if errorlevel 1 (
        echo.
        echo   [错误] 依赖安装失败，请检查网络连接后重试。
        echo.
        pause
        exit /b 1
    )
    echo         依赖安装完成。
)

set "PY=.venv\Scripts\python.exe"

rem ---------- 2. 检查依赖完整性 ----------
"%PY%" -c "import fastapi, uvicorn, numpy, scipy" >nul 2>&1
if errorlevel 1 (
    echo   [2/4] 检测到依赖缺失，正在补装...
    "%PY%" -m pip install -e ".[dev]"
    "%PY%" -c "import fastapi, uvicorn, numpy, scipy" >nul 2>&1
    if errorlevel 1 (
        echo.
        echo   [错误] 依赖不可用，建议删除 .venv 目录后重新运行本文件。
        echo.
        pause
        exit /b 1
    )
    echo         依赖已补齐。
) else (
    echo   [2/4] 依赖检查通过。
)

rem ---------- 3. 检查端口占用（被占用时自动顺延）----------
set "PORTFILE=%TEMP%\galvo_port.txt"
del "%PORTFILE%" >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=%PORT%; if ($p -lt 1 -or $p -gt 65535) { $p=8000 }; $listen=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty LocalPort); if ($listen -notcontains $p) { Set-Content -Path '%PORTFILE%' -Value $p -Encoding ascii } elseif (%FIXED% -eq 1) { Set-Content -Path '%PORTFILE%' -Value 'BUSY' -Encoding ascii } else { $c=$p+1; while ($c -lt 65535 -and $listen -contains $c) { $c++ }; if ($c -lt 65535) { Set-Content -Path '%PORTFILE%' -Value $c -Encoding ascii } else { Set-Content -Path '%PORTFILE%' -Value 'BUSY' -Encoding ascii } }"

set "PICKED="
for /f "usebackq delims=" %%L in ("%PORTFILE%") do set "PICKED=%%L"
del "%PORTFILE%" >nul 2>&1

if "%PICKED%"=="" (
    echo   [错误] 端口探测失败，请改用「启动网页.bat 8010」重试。
    echo.
    pause
    exit /b 1
)
if /i "%PICKED%"=="BUSY" goto :PortBusy

if not "%PICKED%"=="%PORT%" echo   [提示] 端口 %PORT% 已被占用，自动改用 %PICKED%。
set "PORT=%PICKED%"
echo   [3/4] 端口 %PORT% 可用。

rem ---------- 4. 启动服务并自动打开浏览器 ----------
echo   [4/4] 正在启动服务...
echo.
echo   ============================================================
echo    页面地址：http://127.0.0.1:%PORT%
echo    API 文档：http://127.0.0.1:%PORT%/docs
echo.
echo    首次打开页面会自动训练 400 个标定点，耗时约 10~30 秒，请耐心等待。
echo    关闭本窗口即停止服务。
echo   ============================================================
echo.

rem 临时脚本：等接口真正就绪后再打开浏览器，避免出现空白页
set "OPENPS=%TEMP%\galvo_open.ps1"
> "%OPENPS%" echo $port=%PORT%
>>"%OPENPS%" echo $self=$PID
>>"%OPENPS%" echo for ^($i=0; $i -lt 60; $i++^) {
>>"%OPENPS%" echo   $ok=$false
>>"%OPENPS%" echo   try {
>>"%OPENPS%" echo     $r=Invoke-WebRequest -Uri "http://127.0.0.1:$port/api/specifications" -UseBasicParsing -TimeoutSec 2
>>"%OPENPS%" echo     if ^($r.StatusCode -eq 200^) { $ok=$true }
>>"%OPENPS%" echo   } catch { $ok=$false }
>>"%OPENPS%" echo   if ^($ok^) {
>>"%OPENPS%" echo     Start-Process "http://127.0.0.1:$port/"
>>"%OPENPS%" echo     break
>>"%OPENPS%" echo   }
>>"%OPENPS%" echo   if ^(-not ^(Get-Process -Id $self -ErrorAction SilentlyContinue^)^) { break }
>>"%OPENPS%" echo   Start-Sleep -Milliseconds 500
>>"%OPENPS%" echo }

start "" /b powershell -NoProfile -ExecutionPolicy Bypass -File "%OPENPS%"

"%PY%" -m uvicorn five_axis_galvo.api:app --host 127.0.0.1 --port %PORT% --log-level warning
set "EXITCODE=%errorlevel%"

del "%OPENPS%" >nul 2>&1
echo.
if not "%EXITCODE%"=="0" (
    echo   [提示] 服务已退出，返回码 %EXITCODE%。
    echo   若提示端口被占用，说明启动期间该端口被其他程序抢占，
    echo   可改用「启动网页.bat 8010」重试。
) else (
    echo   服务已停止。
)
echo.
pause
exit /b %EXITCODE%

rem ============================================================
:PortBusy
echo.
echo   [错误] 端口 %PORT% 被占用，且你已显式指定该端口，不会自动更改。
echo.
echo   占用该端口的进程：
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { $pr=Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue; Write-Host ('     PID ' + $_.OwningProcess + '  ' + $pr.ProcessName) }"
echo.
echo   解决办法：
echo     1^) 换端口运行：启动网页.bat 8010
echo     2^) 结束占用进程：Stop-Process -Id ^<上面显示的 PID^>
echo.
pause
exit /b 1
