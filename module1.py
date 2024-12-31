import streamlit as st
import re
import json
import os
import random
import string

def delete_user_data():
    file_path = "user_data.json"
    if os.path.exists(file_path):
        os.remove(file_path)

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def validate_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15

def generate_access_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def save_user_data(user_id, name, email, phone, access_code):
    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "access_code": access_code
    }
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)
    return user_data

def run_module1():
    delete_user_data()

    st.title('Formulir Pendaftaran Pengguna📝')

    user_id = st.text_input('ID Pengguna')
    name = st.text_input('Nama Lengkap')
    email = st.text_input('Email')
    phone = st.text_input('Nomor Telepon')

    if st.button('Daftar'):
        if not user_id or not name or not email or not phone:
            st.error("Semua kolom harus diisi!")
        elif not validate_email(email):
            st.error("Format email tidak valid!")
        elif not validate_phone(phone):
            st.error("Nomor telepon tidak valid!")
        else:
            access_code = generate_access_code()
            user_data = save_user_data(user_id, name, email, phone, access_code)
            st.success("Pendaftaran berhasil! Data Anda telah disimpan.")
            st.write(f"Kode Akses Anda: **{access_code}**")
            st.info("Gunakan kode akses ini untuk mendaftar kelas.")
