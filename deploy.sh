#!/bin/bash

echo "🚀 بدء عملية النشر للنظام المحاسبي"
echo "=================================="

# التحقق من وجود Git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. يرجى تثبيت Git أولاً"
    exit 1
fi

# إنشاء repository إذا لم يكن موجود
if [ ! -d ".git" ]; then
    echo "📦 إنشاء repository جديد..."
    git init
    git add .
    git commit -m "Initial commit - نظام المحاسبة المتكامل"
    echo "✅ Repository تم إنشاؤه"
fi

# التحقق من وجود GitHub CLI
if command -v gh &> /dev/null; then
    echo "📤 رفع إلى GitHub..."
    
    # التحقق من remote
    if ! git remote get-url origin &> /dev/null; then
        echo "🔗 يرجى ربط repository بـ GitHub أولاً:"
        echo "gh repo create accounting-system --public --source=. --remote=origin --push"
        echo "أو أنشئ repository يدوياً على GitHub"
    else
        git push -u origin main 2>/dev/null || git push -u origin master
        echo "✅ تم رفع الكود بنجاح"
    fi
else
    echo "⚠️  GitHub CLI غير مثبت. يرجى رفع الكود يدوياً إلى GitHub"
fi

echo ""
echo "🌟 الخطوات التالية:"
echo "1. تأكد من رفع الكود إلى GitHub"
echo "2. اذهب إلى railway.app أو render.com"
echo "3. اختر 'Deploy from GitHub repo'"
echo "4. انتظر النشر وانتهيت!"
echo ""
echo "📖 راجع ملف deployment_guide.md للتفاصيل الكاملة"