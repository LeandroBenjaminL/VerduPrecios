"""not yet defined """
from models.product import Product

def test_product_holds_name_and_category():
    """not yet defined """
    product = Product(name="papa", category="fruta")
    assert product.name == "papa"
    assert product.category == "fruta"
