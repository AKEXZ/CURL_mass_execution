@echo off
chcp 65001 >nul
echo ========================================
echo    API批量请求工具 - 快速安装程序
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python环境
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo ✅ Python环境检测成功

echo.
echo 正在检查离线包目录...
if not exist "pkgs" (
    echo ❌ 未找到pkgs目录
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
echo 正在一键安装所有依赖包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 一键安装所有包
pip install --no-index --find-links pkgs --no-deps pkgs\*.whl

if errorlevel 1 (
    echo.
    echo ⚠️  部分包安装失败，尝试逐个安装...
    echo.
    
    REM 逐个安装核心包
    pip install --no-index --find-links pkgs streamlit pandas requests openpyxl numpy
    if errorlevel 1 (
        echo ❌ 核心依赖安装失败
        pause
        exit /b 1
    )
    
    echo ✅ 核心依赖安装成功
) else (
    echo ✅ 所有依赖包安装成功
)

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
echo 📋 已安装 %count% 个包
echo.
echo 🚀 现在可以运行程序了:
echo   python app.py
echo.
echo 💡 提示:
echo   - 如果遇到权限问题，请以管理员身份运行
echo   - 可以重复运行此脚本更新依赖
echo.

pause 