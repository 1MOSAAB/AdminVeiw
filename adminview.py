import streamlit as st
import firebase_admin
from firebase_admin import credentials, db


service_account_info = {
    "type": "service_account",
    "project_id": st.secrets["type"]["project_id"],
    "private_key_id": st.secrets["type"]["private_key_id"],
    "private_key": st.secrets["type"]["private_key"],
    "client_email": st.secrets["type"]["client_email"],
    "client_id": st.secrets["type"]["client_id"],
    "auth_uri": st.secrets["type"]["auth_uri"],
    "token_uri": st.secrets["type"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["type"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["type"]["client_x509_cert_url"],
    "universe_domain": st.secrets["type"]["universe_domain"],
}


# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://read-write-e65d9-default-rtdb.firebaseio.com/"
    })

#--------------------------------------------------------------------------------------- Admin LOGIN ---------------------------------------------------------------------------------------#
st.title("🛒 Firebase Cart Admin Panel")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username == st.secrets["auth"]["username"] and password == st.secrets["auth"]["password"]:
    st.success("✅ Logged in as Admin")

    # Two columns for Add and Delete
    add_col, delete_col = st.columns(2)
    refresh = False

#--------------------------------------------------------------------------------------- Add New Cart ---------------------------------------------------------------------------------------#

    with add_col:
        st.subheader("➕ Add New Cart")
        new_cart_id = st.text_input("Enter new cart ID", key="add")
        if st.button("Add Cart"):
            if new_cart_id:
                db.reference(f"rfid_tags/{new_cart_id}").set("initialized")
                st.success(f"✅ /rfid_tags/{new_cart_id} created.")
                refresh = True
            else:
                st.warning("⚠️ Please enter a valid cart ID.")

#--------------------------------------------------------------------------------------- Delete Existing Cart ---------------------------------------------------------------------------------------#

    with delete_col:
        st.subheader("🗑️ Delete a Cart")
        cart_to_delete = st.text_input("Enter cart ID to delete", key="delete")
        if st.button("Delete Cart"):
            if cart_to_delete:
                db.reference(f"rfid_tags/{cart_to_delete}").delete()
                st.success(f"🗑️ /rfid_tags/{cart_to_delete} deleted.")
                refresh = True
            else:
                st.warning("⚠️ Please enter a cart ID to delete.")

#--------------------------------------------------------------------------------------- View All Carts ---------------------------------------------------------------------------------------#
    
    st.markdown("---")
    st.subheader("📋 All Existing Carts")
    rfid_ref = db.reference("rfid_tags")
    if refresh or True:
        carts = rfid_ref.get()
        if carts:
            for cart_id in carts:
                st.write(f"- {cart_id}")
        else:
            st.write("No carts found.")

else:
    if username or password:
        st.error("❌ Invalid credentials")
