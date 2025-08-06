#!/bin/bash

# xzx 数据采集平台启动脚本 (Linux/macOS)

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 主函数
main() {
    echo "================================================"
    echo "📊 xzx 数据采集平台"
    echo "================================================"
    
    # 检查Python是否安装
    if ! command -v python3 &> /dev/null; then
        print_error "未找到Python3，请确保Python已正确安装"
        print_info "请访问 https://www.python.org/downloads/ 下载安装Python"
        exit 1
    fi
    
    # 检查当前目录
    if [ ! -f "app.py" ]; then
        print_error "请在项目根目录运行此脚本"
        print_info "请确保在xzx项目文件夹中运行start.sh"
        exit 1
    fi
    
    # 检查依赖
    print_info "检查依赖..."
    if ! python3 -c "import streamlit, pandas, requests, openpyxl" 2>/dev/null; then
        print_error "依赖检查失败"
        print_info "请运行: pip install -r config/requirements_core.txt"
        echo
        read -p "是否现在安装依赖？(y/N): " choice
        case "$choice" in 
            y|Y ) 
                print_info "安装依赖..."
                pip install -r config/requirements_core.txt
                if [ $? -ne 0 ]; then
                    print_error "依赖安装失败"
                    exit 1
                fi
                ;;
            * ) 
                print_warning "请先安装依赖再运行"
                exit 1
                ;;
        esac
    fi
    
    print_success "依赖检查通过"
    echo
    print_info "启动 xzx 数据采集平台..."
    print_info "应用将在浏览器中打开"
    print_info "默认地址: http://localhost:8501"
    print_info "按 Ctrl+C 停止应用"
    echo "================================================"
    echo
    
    # 启动Streamlit应用
    python3 -m streamlit run app.py --server.port 8501 --server.address localhost --browser.gatherUsageStats false
    
    if [ $? -ne 0 ]; then
        echo
        print_error "应用启动失败"
        print_info "请检查错误信息并重试"
        exit 1
    fi
    
    echo
    print_info "应用已停止"
}

# 捕获Ctrl+C信号
trap 'echo -e "\n${YELLOW}👋 应用已停止${NC}"; exit 0' INT

# 运行主函数
main 