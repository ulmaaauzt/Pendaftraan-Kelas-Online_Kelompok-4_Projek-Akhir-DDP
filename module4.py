import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def visualize_class_schedule(registered_classes):
    if registered_classes:
        schedule_df = pd.DataFrame(registered_classes)
        schedule_df['start'] = pd.to_datetime(schedule_df['schedule'])
        schedule_df['end'] = schedule_df['start'] + pd.to_timedelta(schedule_df['duration'].str.split().str[0].astype(int), unit='h')

        fig = px.timeline(
            schedule_df,
            x_start="start",
            x_end="end",
            y="name",
            title="Kalender Jadwal Kelas",
            labels={"name": "Nama Kelas", "start": "Mulai", "end": "Selesai"},
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Belum ada kelas yang terdaftar untuk ditampilkan.")


def display_summary():
    st.title("Dashboard :rocket:")

    user_data = load_json_data("user_data.json")
    if not user_data:
        st.error("Data pengguna tidak ditemukan.")
        return
    
    st.subheader("Data Pengguna")
    user_df = pd.DataFrame([user_data])
    st.table(user_df)

    if "age" in user_data:  
        st.subheader("Distribusi Umur Pengguna")
        st.bar_chart(pd.Series([user_data["age"]]))

    user_classes_file = f"{user_data['id']}_classes.json"
    registered_classes = load_json_data(user_classes_file)
    if registered_classes:
        st.subheader("Jadwal Kelas Anda")
        visualize_class_schedule(registered_classes)
    else:
        st.warning("Belum ada kelas yang didaftarkan.")

    st.subheader("Data Kehadiran")
    if "attendance_db" in st.session_state and not st.session_state.attendance_db.empty:
        st.dataframe(st.session_state.attendance_db)
    else:
        st.warning("Belum ada data kehadiran yang tercatat.")

if __name__ == "__main__":
    st.set_page_config(page_title="DASHBOARD", page_icon=":bar_chart:", layout="wide")
    display_summary()
