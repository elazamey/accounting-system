#!/usr/bin/env python3
"""
نظام المحاسبة المتكامل - Python Flask
سهل الصيانة والإصلاح
مطور بواسطة: MiniMax Agent
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'accounting_system_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===========================================
# نماذج قاعدة البيانات
# ===========================================

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    balance = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'balance': self.balance,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d')
        }

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    balance = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'contact_person': self.contact_person,
            'balance': self.balance,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d')
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='قطعة')
    quantity = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5)
    category = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'price': self.price,
            'cost': self.cost,
            'unit': self.unit,
            'quantity': self.quantity,
            'min_stock': self.min_stock,
            'category': self.category,
            'created_date': self.created_date.strftime('%Y-%m-%d')
        }

class SaleInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    invoice_number = db.Column(db.String(50), unique=True)
    date = db.Column(db.Date, default=date.today)
    subtotal = db.Column(db.Float, nullable=False)
    discount_total = db.Column(db.Float, default=0.0)
    tax_total = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Float, default=0.0)
    remaining = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='partial')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer')
    items = db.relationship('SaleItem', backref='invoice', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else '',
            'date': self.date.strftime('%Y-%m-%d'),
            'subtotal': self.subtotal,
            'discount_total': self.discount_total,
            'tax_total': self.tax_total,
            'total': self.total,
            'paid': self.paid,
            'remaining': self.remaining,
            'status': self.status,
            'items': [item.to_dict() for item in self.items]
        }

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sale_invoice.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'quantity': self.quantity,
            'price': self.price,
            'discount': self.discount,
            'total': self.total
        }

class PurchaseInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    invoice_number = db.Column(db.String(50), unique=True)
    date = db.Column(db.Date, default=date.today)
    subtotal = db.Column(db.Float, nullable=False)
    discount_total = db.Column(db.Float, default=0.0)
    tax_total = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Float, default=0.0)
    remaining = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='partial')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    supplier = db.relationship('Supplier')
    items = db.relationship('PurchaseItem', backref='invoice', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else '',
            'date': self.date.strftime('%Y-%m-%d'),
            'subtotal': self.subtotal,
            'discount_total': self.discount_total,
            'tax_total': self.tax_total,
            'total': self.total,
            'paid': self.paid,
            'remaining': self.remaining,
            'status': self.status,
            'items': [item.to_dict() for item in self.items]
        }

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('purchase_invoice.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'quantity': self.quantity,
            'cost': self.cost,
            'discount': self.discount,
            'total': self.total
        }

# ===========================================
#Routes - الصفحة الرئيسية
# ===========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ===========================================
# API - العملاء
# ===========================================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    
    customer = Customer(
        name=data['name'],
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        balance=data.get('balance', 0.0),
        status=data.get('status', 'active')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({'success': True, 'customer': customer.to_dict()})

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    customer.name = data['name']
    customer.phone = data.get('phone', '')
    customer.address = data.get('address', '')
    customer.balance = data.get('balance', 0.0)
    customer.status = data.get('status', 'active')
    
    db.session.commit()
    
    return jsonify({'success': True, 'customer': customer.to_dict()})

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({'success': True})

# ===========================================
# API - الموردين
# ===========================================

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@app.route('/api/suppliers', methods=['POST'])
def add_supplier():
    data = request.get_json()
    
    supplier = Supplier(
        name=data['name'],
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        contact_person=data.get('contact_person', ''),
        balance=data.get('balance', 0.0),
        status=data.get('status', 'active')
    )
    
    db.session.add(supplier)
    db.session.commit()
    
    return jsonify({'success': True, 'supplier': supplier.to_dict()})

@app.route('/api/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()
    
    supplier.name = data['name']
    supplier.phone = data.get('phone', '')
    supplier.address = data.get('address', '')
    supplier.contact_person = data.get('contact_person', '')
    supplier.balance = data.get('balance', 0.0)
    supplier.status = data.get('status', 'active')
    
    db.session.commit()
    
    return jsonify({'success': True, 'supplier': supplier.to_dict()})

@app.route('/api/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    
    return jsonify({'success': True})

# ===========================================
# API - المنتجات
# ===========================================

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    product = Product(
        name=data['name'],
        code=data.get('code', ''),
        price=float(data['price']),
        cost=float(data['cost']),
        unit=data.get('unit', 'قطعة'),
        quantity=int(data.get('quantity', 0)),
        min_stock=int(data.get('min_stock', 5)),
        category=data.get('category', '')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'success': True, 'product': product.to_dict()})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    product.name = data['name']
    product.code = data.get('code', '')
    product.price = float(data['price'])
    product.cost = float(data['cost'])
    product.unit = data.get('unit', 'قطعة')
    product.quantity = int(data.get('quantity', 0))
    product.min_stock = int(data.get('min_stock', 5))
    product.category = data.get('category', '')
    
    db.session.commit()
    
    return jsonify({'success': True, 'product': product.to_dict()})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'success': True})

# ===========================================
# API - فواتير المبيعات
# ===========================================

@app.route('/api/sales', methods=['GET'])
def get_sales():
    sales = SaleInvoice.query.all()
    return jsonify([sale.to_dict() for sale in sales])

@app.route('/api/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    
    # إنشاء رقم الفاتورة تلقائياً
    last_invoice = SaleInvoice.query.order_by(SaleInvoice.id.desc()).first()
    invoice_number = f"S-{datetime.now().strftime('%Y%m%d')}-{last_invoice.id + 1 if last_invoice else 1:04d}"
    
    sale_invoice = SaleInvoice(
        customer_id=data['customer_id'],
        invoice_number=invoice_number,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        subtotal=float(data['subtotal']),
        discount_total=float(data.get('discount_total', 0.0)),
        tax_total=float(data.get('tax_total', 0.0)),
        total=float(data['total']),
        paid=float(data.get('paid', 0.0)),
        remaining=float(data['remaining']),
        status=data.get('status', 'partial')
    )
    
    db.session.add(sale_invoice)
    db.session.flush()  # للحصول على ID الفاتورة
    
    # إضافة عناصر الفاتورة
    for item_data in data['items']:
        sale_item = SaleItem(
            invoice_id=sale_invoice.id,
            product_id=item_data['product_id'],
            quantity=int(item_data['quantity']),
            price=float(item_data['price']),
            discount=float(item_data.get('discount', 0.0)),
            total=float(item_data['total'])
        )
        db.session.add(sale_item)
        
        # تحديث كمية المنتج
        product = Product.query.get(item_data['product_id'])
        if product:
            product.quantity -= int(item_data['quantity'])
    
    # تحديث رصيد العميل
    customer = Customer.query.get(data['customer_id'])
    if customer:
        customer.balance += float(data['remaining'])
    
    db.session.commit()
    
    return jsonify({'success': True, 'invoice': sale_invoice.to_dict()})

# ===========================================
# API - فواتير المشتريات (الجديدة)
# ===========================================

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    purchases = PurchaseInvoice.query.all()
    return jsonify([purchase.to_dict() for purchase in purchases])

@app.route('/api/purchases', methods=['POST'])
def add_purchase():
    data = request.get_json()
    
    # إنشاء رقم الفاتورة تلقائياً
    last_invoice = PurchaseInvoice.query.order_by(PurchaseInvoice.id.desc()).first()
    invoice_number = f"P-{datetime.now().strftime('%Y%m%d')}-{last_invoice.id + 1 if last_invoice else 1:04d}"
    
    purchase_invoice = PurchaseInvoice(
        supplier_id=data['supplier_id'],
        invoice_number=invoice_number,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        subtotal=float(data['subtotal']),
        discount_total=float(data.get('discount_total', 0.0)),
        tax_total=float(data.get('tax_total', 0.0)),
        total=float(data['total']),
        paid=float(data.get('paid', 0.0)),
        remaining=float(data['remaining']),
        status=data.get('status', 'partial')
    )
    
    db.session.add(purchase_invoice)
    db.session.flush()  # للحصول على ID الفاتورة
    
    # إضافة عناصر الفاتورة
    for item_data in data['items']:
        purchase_item = PurchaseItem(
            invoice_id=purchase_invoice.id,
            product_id=item_data['product_id'],
            quantity=int(item_data['quantity']),
            cost=float(item_data['cost']),
            discount=float(item_data.get('discount', 0.0)),
            total=float(item_data['total'])
        )
        db.session.add(purchase_item)
        
        # تحديث كمية المنتج (زيادة المخزون)
        product = Product.query.get(item_data['product_id'])
        if product:
            product.quantity += int(item_data['quantity'])
    
    # تحديث رصيد المورد
    supplier = Supplier.query.get(data['supplier_id'])
    if supplier:
        supplier.balance += float(data['remaining'])
    
    db.session.commit()
    
    return jsonify({'success': True, 'invoice': purchase_invoice.to_dict()})

# ===========================================
# API - إحصائيات لوحة التحكم
# ===========================================

@app.route('/api/dashboard')
def dashboard_data():
    # إجمالي المبيعات
    total_sales = db.session.query(db.func.sum(SaleInvoice.total)).scalar() or 0
    
    # إجمالي المشتريات
    total_purchases = db.session.query(db.func.sum(PurchaseInvoice.total)).scalar() or 0
    
    # إجمالي العملاء
    total_customers = Customer.query.count()
    
    # إجمالي الموردين
    total_suppliers = Supplier.query.count()
    
    # إجمالي المنتجات
    total_products = Product.query.count()
    
    # أقل من المخزون الأدنى
    low_stock = Product.query.filter(Product.quantity <= Product.min_stock).count()
    
    # فواتير المبيعات الأخيرة (10 فواتير)
    recent_sales = SaleInvoice.query.order_by(SaleInvoice.created_date.desc()).limit(10).all()
    recent_sales_data = [sale.to_dict() for sale in recent_sales]
    
    # البيانات للشهر الحالي
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    monthly_sales = db.session.query(db.func.sum(SaleInvoice.total)).filter(
        db.extract('month', SaleInvoice.date) == current_month,
        db.extract('year', SaleInvoice.date) == current_year
    ).scalar() or 0
    
    monthly_purchases = db.session.query(db.func.sum(PurchaseInvoice.total)).filter(
        db.extract('month', PurchaseInvoice.date) == current_month,
        db.extract('year', PurchaseInvoice.date) == current_year
    ).scalar() or 0
    
    return jsonify({
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'total_customers': total_customers,
        'total_suppliers': total_suppliers,
        'total_products': total_products,
        'low_stock': low_stock,
        'monthly_sales': monthly_sales,
        'monthly_purchases': monthly_purchases,
        'recent_sales': recent_sales_data,
        'profit': total_sales - total_purchases
    })

# ===========================================
# تهيئة قاعدة البيانات
# ===========================================

def init_database():
    """إنشاء الجداول وإضافة البيانات التجريبية"""
    db.create_all()
    
    # إضافة بيانات تجريبية إذا لم تكن موجودة
    if Customer.query.count() == 0:
        sample_customers = [
            Customer(name="أحمد محمد علي", phone="01012345678", address="القاهرة، مصر الجديدة"),
            Customer(name="فاطمة أحمد حسن", phone="01098765432", address="الإسكندرية، محطة الرمل"),
            Customer(name="محمد عبدالرحمن", phone="01123456789", address="الجيزة، الدقي")
        ]
        
        for customer in sample_customers:
            db.session.add(customer)
        
        sample_suppliers = [
            Supplier(name="شركة الأهرام للتجارة", phone="01234567890", address="القاهرة، شارع الهرم", contact_person="عمرو أحمد"),
            Supplier(name="مؤسسة النيل للمواد الغذائية", phone="01987654321", address="الإسكندرية، منطقة بركة السبع", contact_person="سارة علي")
        ]
        
        for supplier in sample_suppliers:
            db.session.add(supplier)
        
        sample_products = [
            Product(name="كمبيوتر محمول", code="LAP001", price=15000.0, cost=12000.0, quantity=5, min_stock=2, category="إلكترونيات"),
            Product(name="ماوس لاسلكي", code="MOU001", price=200.0, cost=150.0, quantity=25, min_stock=10, category="إكسسوارات"),
            Product(name="لوحة مفاتيح ميكانيكية", code="KBD001", price=800.0, cost=600.0, quantity=15, min_stock=5, category="إكسسوارات"),
            Product(name="شاشة كمبيوتر 24 بوصة", code="MON001", price=3500.0, cost=2800.0, quantity=8, min_stock=3, category="إلكترونيات")
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()
        print("✅ تم إنشاء قاعدة البيانات وإضافة البيانات التجريبية")

if __name__ == '__main__':
    with app.app_context():
        init_database()
    
    print("🚀 بدء تشغيل نظام المحاسبة Python...")
    print("🌐 يمكن الوصول للنظام على: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)