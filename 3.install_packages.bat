@echo off
chcp 65001 >nul
echo ========================================
echo    API批量请求工具 - 离线包安装程序
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python环境
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检测成功

echo.
echo 正在检查离线包目录...
if not exist "pkgs" (
    echo ❌ 未找到pkgs目录
    echo 请确保pkgs目录存在且包含所需的wheel文件
    pause
    exit /b 1
)

echo ✅ 离线包目录检测成功

echo.
echo 正在统计离线包数量...
set /a count=0
for %%f in (pkgs\*.whl) do set /a count+=1
echo 📦 发现 %count% 个离线包文件（约88个）

echo.
echo 正在安装核心依赖包...
echo.

REM 安装核心依赖
echo [1/6] 安装基础依赖...
pip install --no-index --find-links pkgs setuptools wheel
if errorlevel 1 (
    echo ❌ 基础依赖安装失败
    pause
    exit /b 1
)

echo [2/6] 安装数据处理依赖...
pip install --no-index --find-links pkgs numpy pandas openpyxl xlrd xlsxwriter
if errorlevel 1 (
    echo ❌ 数据处理依赖安装失败
    pause
    exit /b 1
)

echo [3/6] 安装网络请求依赖...
pip install --no-index --find-links pkgs requests urllib3 certifi charset-normalizer idna
if errorlevel 1 (
    echo ❌ 网络请求依赖安装失败
    pause
    exit /b 1
)

echo [4/6] 安装Streamlit相关依赖...
pip install --no-index --find-links pkgs streamlit altair blinker click packaging protobuf pyarrow pydeck tenacity toml tornado tzdata
if errorlevel 1 (
    echo ❌ Streamlit依赖安装失败
    pause
    exit /b 1
)

echo [5/6] 安装其他工具依赖...
pip install --no-index --find-links pkgs attrs cachetools cffi cryptography cycler distro fonttools frozenlist gitdb GitPython h11 httpcore httpx itsdangerous jinja2 jiter jsonschema jsonschema_specifications jwt kiwisolver macholib markupsafe multidict narwhals outcome pillow propcache pycparser pydantic pydantic_core pyparsing referencing rpds_py smmap sniffio sortedcontainers soupsieve svgpath2mpl tqdm trio trio_websocket typing_inspection websocket_client wsproto yarl aiohappyeyeballs aiohttp aiosignal anyio altgraph annotated_types bs4 contourpy flask flask_cors beautifulsoup4 selenium lxml watchdog
if errorlevel 1 (
    echo ❌ 其他工具依赖安装失败
    pause
    exit /b 1
)

echo [6/6] 安装可选依赖...
pip install --no-index --find-links pkgs matplotlib seaborn scipy sklearn opencv-python
if errorlevel 1 (
    echo ⚠️  可选依赖安装失败（不影响核心功能）
)

echo.
echo ✅ 所有依赖包安装完成！

echo.
echo 正在验证安装...
python -c "import streamlit, pandas, requests, openpyxl; print('✅ 核心依赖验证成功')"
if errorlevel 1 (
    echo ❌ 依赖验证失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 📋 已安装的包:
echo   - 数据处理: numpy, pandas, openpyxl, xlrd, xlsxwriter
echo   - 网络请求: requests, urllib3, certifi
echo   - Web框架: streamlit, altair, tornado
echo   - 工具库: cryptography, jinja2, pydantic
echo   - 其他: 共 %count% 个包
echo.
echo 🚀 现在可以运行程序了:
echo   python app.py
echo   或
echo   python start.py
echo.
echo 💡 提示:
echo   - 如果遇到权限问题，请以管理员身份运行
echo   - 如果某些包安装失败，不影响核心功能
echo   - 可以重复运行此脚本更新依赖
echo.

pause 