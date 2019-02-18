from app import app, db



from blueprints.core.models import Product, Brand, Category, Variant

@app.shell_context_processor
def shell_context():
    return {'Category': Category, 'Product': Product, 'db': db, 'Brand': Brand, 'Variant': Variant}

