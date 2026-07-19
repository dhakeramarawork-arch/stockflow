import os

# Define all directories and files based on the architecture
structure = {
    "dirs": [
        "inventory_system", "core/migrations", "accounts/migrations", 
        "dashboard/migrations", "categories/migrations", "brands/migrations", 
        "units/migrations", "products/migrations", "suppliers/migrations", 
        "customers/migrations", "purchases/migrations", "sales/migrations", 
        "inventory/migrations", "reports/migrations",
        "templates", "templates/core", "templates/partials", "templates/accounts", 
        "templates/dashboard", "templates/categories", "templates/brands", 
        "templates/units", "templates/products", "templates/suppliers", 
        "templates/customers", "templates/purchases", "templates/sales", 
        "templates/inventory", "templates/reports",
        "static/css", "static/js"
    ],
    "files": [
        "manage.py", "requirements.txt", "setup_and_run.sh",
        "inventory_system/__init__.py", "inventory_system/settings.py", 
        "inventory_system/urls.py", "inventory_system/wsgi.py", "inventory_system/asgi.py",
        "core/__init__.py", "core/apps.py", "core/urls.py", "core/views.py", 
        "core/utils.py", "core/decorators.py", "core/context_processors.py",
        "core/migrations/__init__.py",
        "accounts/__init__.py", "accounts/apps.py", "accounts/urls.py", 
        "accounts/views.py", "accounts/models.py", "accounts/forms.py", 
        "accounts/admin.py", "accounts/signals.py", "accounts/migrations/__init__.py",
        "dashboard/__init__.py", "dashboard/apps.py", "dashboard/urls.py", 
        "dashboard/views.py", "dashboard/migrations/__init__.py",
        "categories/__init__.py", "categories/apps.py", "categories/urls.py", 
        "categories/views.py", "categories/models.py", "categories/forms.py", 
        "categories/admin.py", "categories/migrations/__init__.py",
        "brands/__init__.py", "brands/apps.py", "brands/urls.py", 
        "brands/views.py", "brands/models.py", "brands/forms.py", 
        "brands/admin.py", "brands/migrations/__init__.py",
        "units/__init__.py", "units/apps.py", "units/urls.py", 
        "units/views.py", "units/models.py", "units/forms.py", 
        "units/admin.py", "units/migrations/__init__.py",
        "products/__init__.py", "products/apps.py", "products/urls.py", 
        "products/views.py", "products/models.py", "products/forms.py", 
        "products/admin.py", "products/migrations/__init__.py",
        "suppliers/__init__.py", "suppliers/apps.py", "suppliers/urls.py", 
        "suppliers/views.py", "suppliers/models.py", "suppliers/forms.py", 
        "suppliers/admin.py", "suppliers/migrations/__init__.py",
        "customers/__init__.py", "customers/apps.py", "customers/urls.py", 
        "customers/views.py", "customers/models.py", "customers/forms.py", 
        "customers/admin.py", "customers/migrations/__init__.py",
        "purchases/__init__.py", "purchases/apps.py", "purchases/urls.py", 
        "purchases/views.py", "purchases/models.py", "purchases/forms.py", 
        "purchases/admin.py", "purchases/migrations/__init__.py",
        "sales/__init__.py", "sales/apps.py", "sales/urls.py", 
        "sales/views.py", "sales/models.py", "sales/forms.py", 
        "sales/admin.py", "sales/migrations/__init__.py",
        "inventory/__init__.py", "inventory/apps.py", "inventory/urls.py", 
        "inventory/views.py", "inventory/models.py", "inventory/forms.py", 
        "inventory/admin.py", "inventory/migrations/__init__.py",
        "reports/__init__.py", "reports/apps.py", "reports/urls.py", 
        "reports/views.py", "reports/migrations/__init__.py",
        "templates/base.html", "templates/dashboard_base.html",
        "templates/partials/sidebar.html", "templates/partials/navbar.html", 
        "templates/partials/footer.html", "templates/partials/messages.html", 
        "templates/partials/pagination.html",
        "templates/core/home.html", "templates/core/404.html", "templates/core/500.html",
        "templates/accounts/login.html", "templates/accounts/profile.html", 
        "templates/accounts/change_password.html", "templates/accounts/forgot_password.html",
        "templates/dashboard/dashboard.html",
        "templates/categories/category_list.html", "templates/categories/category_form.html", 
        "templates/categories/category_confirm_delete.html",
        "templates/brands/brand_list.html", "templates/brands/brand_form.html", 
        "templates/brands/brand_confirm_delete.html",
        "templates/units/unit_list.html", "templates/units/unit_form.html", 
        "templates/units/unit_confirm_delete.html",
        "templates/products/product_list.html", "templates/products/product_form.html", 
        "templates/products/product_detail.html", "templates/products/product_confirm_delete.html",
        "templates/suppliers/supplier_list.html", "templates/suppliers/supplier_form.html", 
        "templates/suppliers/supplier_confirm_delete.html",
        "templates/customers/customer_list.html", "templates/customers/customer_form.html", 
        "templates/customers/customer_confirm_delete.html",
        "templates/purchases/purchase_list.html", "templates/purchases/purchase_form.html", 
        "templates/purchases/purchase_detail.html", "templates/purchases/purchase_confirm_delete.html",
        "templates/sales/sale_list.html", "templates/sales/sale_form.html", 
        "templates/sales/sale_detail.html", "templates/sales/sale_confirm_delete.html",
        "templates/inventory/overview.html", "templates/inventory/movements.html", 
        "templates/inventory/adjustment_form.html",
        "templates/reports/index.html", "templates/reports/sales_report.html",
        "static/css/style.css", "static/js/main.js"
    ]
}

print("Creating project structure...")

for d in structure["dirs"]:
    os.makedirs(d, exist_ok=True)
    print(f"Created directory: {d}")

for f in structure["files"]:
    os.makedirs(os.path.dirname(f), exist_ok=True) if os.path.dirname(f) else None
    with open(f, 'w', encoding='utf-8') as file:
        file.write("") # Create empty file
    print(f"Created file: {f}")

print("\n✅ Project structure created successfully!")
print("Next step: Copy the code from my previous message into these files.")