#!/bin/bash

# نظام المحاسبة المتكامل - Python Flask
# سكريبت التشغيل والإعداد
# Developed by: MiniMax Agent

echo "🚀 بدء تشغيل نظام المحاسبة المتكامل - Python Edition"
echo "=================================================="

# التحقق من Python
if ! command -v python &> /dev/null; then
    echo "❌ Python غير مثبت. يرجى تثبيت Python أولاً"
    exit 1
fi

echo "✅ Python متوفر: $(python --version)"

# التحقق من pip
if ! command -v pip &> /dev/null && ! command -v uv &> /dev/null; then
    echo "❌ pip أو uv غير متوفر. يرجى تثبيت أحدهما"
    exit 1
fi

echo "✅ مدير الحزم متوفر"

# تثبيت المتطلبات إذا لم تكن مثبتة
if [ ! -f ".requirements_installed" ]; then
    echo "📦 تثبيت المتطلبات..."
    
    if command -v uv &> /dev/null; then
        uv add flask flask-sqlalchemy
    else
        pip install flask flask-sqlalchemy
    fi
    
    touch .requirements_installed
    echo "✅ تم تثبيت المتطلبات"
fi

# تشغيل النظام
echo "🌐 بدء تشغيل الخادم..."
echo "📱 يمكن الوصول للنظام على: http://localhost:5000"
echo ""
echo "🔧 للإيقاف: اضغط Ctrl+C"
echo "=================================================="

# تشغيل Flask
python app.py