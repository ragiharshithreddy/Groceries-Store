import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="FreshMart - Online Grocery Store",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        padding: 1rem 0;
        font-weight: bold;
    }
    .product-card {
        border: 2px solid #E8F5E9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #F1F8E9;
    }
    .category-header {
        color: #1B5E20;
        font-size: 1.8rem;
        margin-top: 1rem;
        border-bottom: 3px solid #66BB6A;
        padding-bottom: 0.5rem;
    }
    .cart-item {
        background-color: #E8F5E9;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    .price-tag {
        color: #2E7D32;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .stock-badge {
        background-color: #81C784;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Product database
PRODUCTS = {
    "Fruits & Vegetables": [
        {"id": "F001", "name": "Fresh Apples", "price": 3.99, "unit": "per kg", "stock": 50, "image": "🍎"},
        {"id": "F002", "name": "Bananas", "price": 2.49, "unit": "per kg", "stock": 80, "image": "🍌"},
        {"id": "F003", "name": "Oranges", "price": 4.29, "unit": "per kg", "stock": 60, "image": "🍊"},
        {"id": "F004", "name": "Fresh Tomatoes", "price": 3.49, "unit": "per kg", "stock": 45, "image": "🍅"},
        {"id": "F005", "name": "Carrots", "price": 2.99, "unit": "per kg", "stock": 70, "image": "🥕"},
        {"id": "F006", "name": "Broccoli", "price": 3.79, "unit": "per kg", "stock": 35, "image": "🥦"},
    ],
    "Dairy & Eggs": [
        {"id": "D001", "name": "Fresh Milk", "price": 4.99, "unit": "per liter", "stock": 100, "image": "🥛"},
        {"id": "D002", "name": "Cheddar Cheese", "price": 6.99, "unit": "per 500g", "stock": 40, "image": "🧀"},
        {"id": "D003", "name": "Greek Yogurt", "price": 3.49, "unit": "per 500g", "stock": 60, "image": "🥛"},
        {"id": "D004", "name": "Fresh Eggs", "price": 5.99, "unit": "per dozen", "stock": 120, "image": "🥚"},
        {"id": "D005", "name": "Butter", "price": 4.49, "unit": "per 250g", "stock": 55, "image": "🧈"},
    ],
    "Bakery": [
        {"id": "B001", "name": "Whole Wheat Bread", "price": 2.99, "unit": "per loaf", "stock": 75, "image": "🍞"},
        {"id": "B002", "name": "Croissants", "price": 4.99, "unit": "per pack of 6", "stock": 30, "image": "🥐"},
        {"id": "B003", "name": "Bagels", "price": 3.99, "unit": "per pack of 6", "stock": 45, "image": "🥯"},
        {"id": "B004", "name": "Muffins", "price": 5.49, "unit": "per pack of 4", "stock": 40, "image": "🧁"},
    ],
    "Meat & Seafood": [
        {"id": "M001", "name": "Chicken Breast", "price": 8.99, "unit": "per kg", "stock": 50, "image": "🍗"},
        {"id": "M002", "name": "Ground Beef", "price": 10.99, "unit": "per kg", "stock": 45, "image": "🥩"},
        {"id": "M003", "name": "Fresh Salmon", "price": 15.99, "unit": "per kg", "stock": 25, "image": "🐟"},
        {"id": "M004", "name": "Shrimp", "price": 12.99, "unit": "per kg", "stock": 30, "image": "🦐"},
    ],
    "Beverages": [
        {"id": "BEV001", "name": "Orange Juice", "price": 4.49, "unit": "per liter", "stock": 80, "image": "🧃"},
        {"id": "BEV002", "name": "Green Tea", "price": 3.99, "unit": "per box", "stock": 60, "image": "🍵"},
        {"id": "BEV003", "name": "Coffee Beans", "price": 9.99, "unit": "per 500g", "stock": 40, "image": "☕"},
        {"id": "BEV004", "name": "Mineral Water", "price": 2.99, "unit": "per 6-pack", "stock": 150, "image": "💧"},
    ]
}

def add_to_cart(product_id, product_name, price, quantity):
    """Add item to cart"""
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id]['quantity'] += quantity
    else:
        st.session_state.cart[product_id] = {
            'name': product_name,
            'price': price,
            'quantity': quantity
        }

def remove_from_cart(product_id):
    """Remove item from cart"""
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def calculate_total():
    """Calculate cart total"""
    total = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
    return total

def display_product(product, category):
    """Display individual product"""
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    
    with col1:
        st.markdown(f"<div style='font-size: 3rem;'>{product['image']}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{product['name']}**")
        st.caption(f"ID: {product['id']}")
    
    with col3:
        st.markdown(f"<span class='price-tag'>${product['price']:.2f}</span>", unsafe_allow_html=True)
        st.caption(product['unit'])
        st.markdown(f"<span class='stock-badge'>Stock: {product['stock']}</span>", unsafe_allow_html=True)
    
    with col4:
        quantity = st.number_input(
            "Qty", 
            min_value=1, 
            max_value=product['stock'], 
            value=1, 
            key=f"qty_{product['id']}"
        )
        if st.button("🛒 Add to Cart", key=f"add_{product['id']}"):
            add_to_cart(product['id'], product['name'], product['price'], quantity)
            st.success(f"Added {quantity} x {product['name']} to cart!")
            st.rerun()

# Header
st.markdown("<h1 class='main-header'>🛒 FreshMart Online Grocery Store</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Shopping Cart
with st.sidebar:
    st.header("🛒 Shopping Cart")
    
    if st.session_state.cart:
        for product_id, item in st.session_state.cart.items():
            st.markdown(f"""
            <div class='cart-item'>
                <strong>{item['name']}</strong><br>
                ${item['price']:.2f} x {item['quantity']} = ${item['price'] * item['quantity']:.2f}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"❌ Remove", key=f"remove_{product_id}"):
                remove_from_cart(product_id)
                st.rerun()
            
            st.markdown("---")
        
        # Cart Summary
        total = calculate_total()
        st.markdown(f"### Total: ${total:.2f}")
        
        if st.button("🚀 Proceed to Checkout", type="primary", use_container_width=True):
            st.session_state.show_checkout = True
            st.rerun()
            
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    else:
        st.info("Your cart is empty")

# Main Content
tab1, tab2, tab3 = st.tabs(["🏪 Shop", "🧾 Checkout", "📦 Orders"])

with tab1:
    # Search and Filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search products", placeholder="Search by name...")
    with col2:
        selected_category = st.selectbox("Category", ["All"] + list(PRODUCTS.keys()))
    
    # Display Products
    categories_to_show = PRODUCTS.keys() if selected_category == "All" else [selected_category]
    
    for category in categories_to_show:
        st.markdown(f"<h2 class='category-header'>{category}</h2>", unsafe_allow_html=True)
        
        products = PRODUCTS[category]
        
        # Filter by search query
        if search_query:
            products = [p for p in products if search_query.lower() in p['name'].lower()]
        
        if products:
            for product in products:
                with st.container():
                    display_product(product, category)
                    st.markdown("---")
        else:
            st.info("No products found")

with tab2:
    st.header("🧾 Checkout")
    
    if st.session_state.cart:
        # Order Summary
        st.subheader("Order Summary")
        for product_id, item in st.session_state.cart.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(item['name'])
            with col2:
                st.write(f"Qty: {item['quantity']}")
            with col3:
                st.write(f"${item['price'] * item['quantity']:.2f}")
        
        st.markdown("---")
        total = calculate_total()
        st.markdown(f"### **Total Amount: ${total:.2f}**")
        
        # Customer Information
        st.subheader("Customer Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
        
        with col2:
            address = st.text_area("Delivery Address*")
            city = st.text_input("City*")
            postal_code = st.text_input("Postal Code*")
        
        # Payment Method
        st.subheader("Payment Method")
        payment_method = st.radio(
            "Select payment method",
            ["Credit/Debit Card", "Cash on Delivery", "PayPal", "Bank Transfer"]
        )
        
        # Place Order
        if st.button("✅ Place Order", type="primary", use_container_width=True):
            if name and email and phone and address and city and postal_code:
                order = {
                    'order_id': f"ORD{len(st.session_state.orders) + 1:04d}",
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'customer': {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'address': address,
                        'city': city,
                        'postal_code': postal_code
                    },
                    'items': st.session_state.cart.copy(),
                    'total': total,
                    'payment_method': payment_method,
                    'status': 'Confirmed'
                }
                
                st.session_state.orders.append(order)
                st.session_state.cart = {}
                
                st.success(f"✅ Order placed successfully! Order ID: {order['order_id']}")
                st.balloons()
                st.info("Your order will be delivered within 2-3 business days.")
            else:
                st.error("Please fill in all required fields")
    else:
        st.info("Your cart is empty. Add some items to checkout!")

with tab3:
    st.header("📦 Your Orders")
    
    if st.session_state.orders:
        for order in reversed(st.session_state.orders):
            with st.expander(f"Order #{order['order_id']} - {order['date']} - Status: {order['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Customer Details")
                    st.write(f"**Name:** {order['customer']['name']}")
                    st.write(f"**Email:** {order['customer']['email']}")
                    st.write(f"**Phone:** {order['customer']['phone']}")
                    st.write(f"**Address:** {order['customer']['address']}, {order['customer']['city']}")
                    st.write(f"**Postal Code:** {order['customer']['postal_code']}")
                
                with col2:
                    st.subheader("Order Details")
                    st.write(f"**Payment Method:** {order['payment_method']}")
                    st.write(f"**Total Amount:** ${order['total']:.2f}")
                    st.write(f"**Status:** {order['status']}")
                
                st.subheader("Items")
                for product_id, item in order['items'].items():
                    st.write(f"- {item['name']}: {item['quantity']} x ${item['price']:.2f} = ${item['price'] * item['quantity']:.2f}")
    else:
        st.info("You haven't placed any orders yet.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>🛒 <strong>FreshMart Online Grocery Store</strong></p>
    <p>Fresh produce delivered to your doorstep | Open 24/7</p>
    <p>Contact us: support@freshmart.com | +1-800-FRESH-99</p>
</div>
""", unsafe_allow_html=True)
