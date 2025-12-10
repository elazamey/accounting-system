#!/usr/bin/env python3
"""
نظام اختبار برنامج المحاسبة
يقوم بفتح التطبيق وإضافة بيانات تجريبية
"""

import time
import json
import sqlite3
from pathlib import Path

def create_sample_data():
    """إنشاء بيانات تجريبية لاختبار النظام"""
    
    # بيانات العملاء
    customers = [
        {
            "name": "أحمد محمد علي",
            "phone": "01012345678",
            "address": "القاهرة، مصر الجديدة",
            "balance": 0.0,
            "status": "active"
        },
        {
            "name": "فاطمة أحمد حسن", 
            "phone": "01098765432",
            "address": "الإسكندرية، محطة الرمل",
            "balance": 500.0,
            "status": "active"
        },
        {
            "name": "محمد عبدالرحمن",
            "phone": "01123456789", 
            "address": "الجيزة، الدقي",
            "balance": -200.0,
            "status": "active"
        }
    ]
    
    # بيانات الموردين
    suppliers = [
        {
            "name": "شركة الأهرام للتجارة",
            "phone": "01234567890",
            "address": "القاهرة، شارع الهرم",
            "contact_person": "عمرو أحمد",
            "balance": 0.0,
            "status": "active"
        },
        {
            "name": "مؤسسة النيل للمواد الغذائية",
            "phone": "01987654321",
            "address": "الإسكندرية، منطقة بركة السبع",
            "contact_person": "سارة علي",
            "balance": 1200.0,
            "status": "active"
        }
    ]
    
    # بيانات المنتجات
    products = [
        {
            "name": "كمبيوتر محمول",
            "code": "LAP001",
            "price": 15000.0,
            "cost": 12000.0,
            "unit": "قطعة",
            "quantity": 5,
            "min_stock": 2,
            "category": "إلكترونيات"
        },
        {
            "name": "ماوس لاسلكي",
            "code": "MOU001", 
            "price": 200.0,
            "cost": 150.0,
            "unit": "قطعة",
            "quantity": 25,
            "min_stock": 10,
            "category": "إكسسوارات"
        },
        {
            "name": "لوحة مفاتيح ميكانيكية",
            "code": "KBD001",
            "price": 800.0,
            "cost": 600.0,
            "unit": "قطعة", 
            "quantity": 15,
            "min_stock": 5,
            "category": "إكسسوارات"
        },
        {
            "name": "شاشة كمبيوتر 24 بوصة",
            "code": "MON001",
            "price": 3500.0,
            "cost": 2800.0,
            "unit": "قطعة",
            "quantity": 8,
            "min_stock": 3,
            "category": "إلكترونيات"
        }
    ]
    
    # بيانات فواتير المبيعات
    sales_invoices = [
        {
            "customer_id": 1,
            "date": "2025-11-10",
            "items": [
                {"product_id": 1, "quantity": 1, "price": 15000.0, "discount": 0},
                {"product_id": 2, "quantity": 1, "price": 200.0, "discount": 0}
            ],
            "subtotal": 15200.0,
            "discount_total": 0,
            "tax_total": 0,
            "total": 15200.0,
            "paid": 15200.0,
            "remaining": 0.0,
            "status": "completed"
        },
        {
            "customer_id": 2, 
            "date": "2025-11-09",
            "items": [
                {"product_id": 3, "quantity": 1, "price": 800.0, "discount": 50},
                {"product_id": 4, "quantity": 2, "price": 3500.0, "discount": 0}
            ],
            "subtotal": 7800.0,
            "discount_total": 50.0,
            "tax_total": 0,
            "total": 7750.0,
            "paid": 5000.0,
            "remaining": 2750.0,
            "status": "partial"
        }
    ]
    
    return {
        'customers': customers,
        'suppliers': suppliers, 
        'products': products,
        'sales_invoices': sales_invoices
    }

def test_html_file():
    """اختبار وجود ملف HTML"""
    html_path = Path("/workspace/index.html")
    if html_path.exists():
        print("✅ ملف index.html موجود")
        size = html_path.stat().st_size
        print(f"📄 حجم الملف: {size:,} بايت")
        return True
    else:
        print("❌ ملف index.html غير موجود")
        return False

def test_javascript_files():
    """اختبار وجود ملفات JavaScript"""
    js_dir = Path("/workspace/js")
    js_files = [
        "app.js", "dashboard.js", "customers.js", "suppliers.js", 
        "sales.js", "reports.js", "settings.js", "database.js", "utils.js"
    ]
    
    all_exist = True
    for file in js_files:
        file_path = js_dir / file
        if file_path.exists():
            print(f"✅ {file} موجود")
        else:
            print(f"❌ {file} غير موجود")
            all_exist = False
    
    return all_exist

def test_css_files():
    """اختبار وجود ملفات CSS"""
    css_dir = Path("/workspace/styles")
    css_files = ["main.css", "components.css", "responsive.css"]
    
    all_exist = True
    for file in css_files:
        file_path = css_dir / file
        if file_path.exists():
            print(f"✅ {file} موجود")
        else:
            print(f"❌ {file} غير موجود")
            all_exist = False
    
    return all_exist

def generate_test_report():
    """إنشاء تقرير الاختبار"""
    print("="*50)
    print("🧪 تقرير اختبار برنامج المحاسبة")
    print("="*50)
    
    # اختبار الملفات
    print("\n📁 اختبار وجود الملفات:")
    html_ok = test_html_file()
    js_ok = test_javascript_files()
    css_ok = test_css_files()
    
    print(f"\n📊 ملخص الاختبار:")
    print(f"   HTML: {'✅ نجح' if html_ok else '❌ فشل'}")
    print(f"   JavaScript: {'✅ نجح' if js_ok else '❌ فشل'}")
    print(f"   CSS: {'✅ نجح' if css_ok else '❌ فشل'}")
    
    if html_ok and js_ok and css_ok:
        print("\n🎉 جميع الملفات موجودة وجاهزة للاختبار!")
        print("🌐 يمكن فتح النظام على: http://localhost:8000")
    else:
        print("\n⚠️  بعض الملفات مفقودة")
    
    # إنشاء البيانات التجريبية
    print(f"\n📋 إنشاء البيانات التجريبية:")
    sample_data = create_sample_data()
    
    # حفظ البيانات في ملف JSON
    data_file = Path("/workspace/sample_data.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    print(f"✅ تم إنشاء ملف البيانات التجريبية: {data_file}")
    
    return html_ok and js_ok and css_ok

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء اختبار نظام المحاسبة...")
    
    # إنشاء تقرير الاختبار
    system_ready = generate_test_report()
    
    print(f"\n" + "="*50)
    if system_ready:
        print("🎯 الخطوات التالية:")
        print("1. فتح http://localhost:8000 في المتصفح")
        print("2. اختبار الإضافة والتعديل والحذف للعملاء")
        print("3. اختبار إنشاء فاتورة مبيعات")
        print("4. مراجعة التقارير والإحصائيات")
        print("5. تطوير وحدة المشتريات")
    else:
        print("⚠️  النظام غير جاهز - يرجى التحقق من الملفات")
    print("="*50)
    
    return system_ready

if __name__ == "__main__":
    main()