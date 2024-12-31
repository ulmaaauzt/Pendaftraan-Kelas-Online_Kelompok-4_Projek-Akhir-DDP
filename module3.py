import streamlit as st
import re
import json
import os
import random
import string
import pandas as pd
import qrcode
from datetime import datetime
import io
from PIL import Image
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def mark_attendance(student_id, student_name, class_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success(f"Kehadiran {student_name} di kelas {class_name} telah dicatat pada {timestamp}.")

def delete_user_data():
    file_path = "user_data.json"
    if os.path.exists(file_path):
        os.remove(file_path)

def delete_registered_classes():
    file_path = "registered_classes.json"
    if os.path.exists(file_path):
        os.remove(file_path)

def save_attendance_to_file():
    attendance_file = "attendance_records.json"
    if os.path.exists(attendance_file):
        with open(attendance_file, "r") as f:
            try:
                attendance_data = json.load(f)
            except json.JSONDecodeError:
                attendance_data = []
    else:
        attendance_data = []

    new_records = st.session_state.attendance_db.to_dict(orient="records")
    attendance_data.extend(new_records)

    with open(attendance_file, "w") as f:
        json.dump(attendance_data, f)
    st.success("Data kehadiran telah disimpan ke file.")

def visualize_class_schedule(registered_classes):
    st.subheader("Kalender Jadwal Kelas")
    if registered_classes:
        schedule_df = pd.DataFrame(registered_classes)
        schedule_df['start'] = pd.to_datetime(schedule_df['schedule'])
        schedule_df['end'] = schedule_df['start'] + pd.to_timedelta(schedule_df['duration'].str.split().str[0].astype(int), unit='h')

        fig = px.timeline(
            schedule_df,
            x_start="start",
            x_end="end",
            y="name",
            title="Jadwal Kelas Anda",
            labels={"name": "Nama Kelas", "start": "Mulai", "end": "Selesai"},
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Belum ada kelas yang terdaftar untuk ditampilkan.")


def run_module1():
    delete_user_data()

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

    st.title('Formulir Pendaftaran Pengguna')

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
            st.json(user_data)
            st.write(f"Kode Akses Anda: **{access_code}**")
            st.info("Gunakan kode akses ini untuk mendaftar kelas.")

def run_module2():
    delete_registered_classes()

    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = None

    st.title('Daftar Kelas dan Jadwal\U0001F469\u200D\U0001F3EB')

    if not user_data:
        st.error("Silakan daftar terlebih dahulu di modul Pendaftaran Pengguna.")
        st.stop()

    st.write(f"Selamat datang, {user_data['name']}!")

    if "access_verified" not in st.session_state:
        st.session_state.access_verified = False

    if not st.session_state.access_verified:
        access_code_input = st.text_input("Masukkan Kode Akses Anda untuk melanjutkan")
        if st.button("Verifikasi Kode Akses"):
            if access_code_input == user_data["access_code"]:
                st.success("Kode akses valid. Anda dapat melanjutkan.")
                st.session_state.access_verified = True
            else:
                st.error("Kode akses salah atau tidak valid. Harap periksa kembali.")
    else:
        available_classes = [
            {"id": 1, "name": "Bahasa Indonesia", "description": "Kelas Bahasa Indonesia untuk pemula", "duration": "1 Jam", "schedule": "2024-12-20 10:00"},
            {"id": 2, "name": "Bahasa Inggris", "description": "Kelas Bahasa Inggris dasar", "duration": "1 Jam", "schedule": "2024-12-21 14:00"},
            {"id": 3, "name": "Matematika", "description": "Kelas Matematika tingkat dasar", "duration": "2 Jam", "schedule": "2024-12-22 08:00"},
            {"id": 4, "name": "IPA", "description": "Kelas Ilmu Pengetahuan Alam", "duration": "1.5 Jam", "schedule": "2024-12-23 16:00"},
            {"id": 5, "name": "IPS", "description": "Kelas Ilmu Pengetahuan Sosial", "duration": "1 Jam", "schedule": "2024-12-24 13:00"}
        ]

        user_classes_file = f"{user_data['id']}_classes.json"
        if os.path.exists(user_classes_file):
            with open(user_classes_file, "r") as f:
                selected_classes = json.load(f)
        else:
            selected_classes = []

        if selected_classes:
            st.warning(f"Anda sudah terdaftar di kelas: **{selected_classes[0]['name']}**.")
            visualize_class_schedule(selected_classes)
            st.stop()

        st.subheader('Kelas yang Tersedia')

        selected_class_name = st.selectbox(
            "Pilih Kelas:",
            [cls["name"] for cls in available_classes]
        )

        selected_class = next((cls for cls in available_classes if cls["name"] == selected_class_name), None)

        if st.button("Daftar"):
            if selected_class:
                with open(user_classes_file, "w") as f:
                    json.dump([selected_class], f)
                st.success(f"Berhasil mendaftar ke kelas **{selected_class['name']}**.")
                st.write("Detail Jadwal:")
                st.write(f"- **Nama Kelas:** {selected_class['name']}")
                st.write(f"- **Deskripsi:** {selected_class['description']}")
                st.write(f"- **Durasi:** {selected_class['duration']}")
                st.write(f"- **Jadwal:** {selected_class['schedule']}")

                visualize_class_schedule([selected_class])
            else:
                st.error("Kelas tidak ditemukan. Silakan coba lagi.")

def run_module3():
    if "attendance_db" not in st.session_state:
        st.session_state.attendance_db = pd.DataFrame(columns=["student_id", "name", "class_name", "timestamp"])

    st.title('Pengecekan Kehadiran🖥️')

    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        st.error("Silakan daftar terlebih dahulu di modul Pendaftaran Pengguna.")
        st.stop()

    user_classes_file = f"{user_data['id']}_classes.json"
    if os.path.exists(user_classes_file):
        with open(user_classes_file, "r") as f:
            try:
                selected_classes = json.load(f)
            except json.JSONDecodeError:
                selected_classes = []
    else:
        selected_classes = []

    if not selected_classes:
        st.error("Anda belum mendaftar kelas. Silakan daftar kelas terlebih dahulu.")
        st.stop()

    def mark_attendance(student_id, student_name, class_name):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame([{ 
            "student_id": student_id, 
            "name": student_name, 
            "class_name": class_name, 
            "timestamp": timestamp 
        }])
        st.session_state.attendance_db = pd.concat([st.session_state.attendance_db, new_data], ignore_index=True)
        st.success(f"Kehadiran {student_name} di kelas {class_name} telah dicatat pada {timestamp}.")

    st.subheader('Pilih Kelas untuk Absensi')
    class_choice = st.selectbox("Pilih Kelas:", [cls["name"] for cls in selected_classes])

    student_id = st.selectbox("Pilih ID:", [user_data["id"]])
    student_name = st.selectbox("Pilih Nama:", [user_data["name"]])

    if st.button(f"Absen di Kelas {class_choice}"):
        if student_id == user_data["id"] and student_name.strip().lower() == user_data["name"].strip().lower():
            mark_attendance(student_id, student_name, class_choice)
        else:
            st.error("ID atau Nama salah. Harap periksa kembali.")

    st.subheader('Data Kehadiran')
    if not st.session_state.attendance_db.empty:
        st.write("Berikut adalah data kehadiran yang tercatat:")
        st.dataframe(st.session_state.attendance_db)
    else:
        st.write("Belum ada data kehadiran yang tercatat.")
