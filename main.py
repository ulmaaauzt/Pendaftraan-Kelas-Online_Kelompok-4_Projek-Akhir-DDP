import streamlit as st

st.set_page_config(
    page_title="Pendaftaran Kelas Online", 
    page_icon=":rocket:", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(#16D9E8, #C3DDEB);   
            background-attachment: fixed;
            font-family: Arial, sans-serif;
        }
        .main {
            background: linear-gradient(135deg, #6A1B9A, #D81B60);
            color: white;
            padding: 20px;
            border-radius: 10px;
            font-family: Arial, sans-serif;
        }
        .stSidebar {
            background-image: linear-gradient(#16D9E8, #C3DDEB, #EEE3EC, #FBBDBA);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#444444; font-family: Classic; font-size: 30px; text-align: center;'>Navigasi</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>Pilih menu yang ingin dijalankan:</p>", unsafe_allow_html=True)

menu_options = ["📝 Pendaftaran", "👩‍🏫 Daftar Kelas", "🖥️ Absensi", "🌐 Dashboard"]

page = st.sidebar.selectbox(
    label="Menu", 
    options=menu_options,
    index=0,
    help="Navigasikan ke modul yang diinginkan"
)

if page == "📝 Pendaftaran":
    from module1 import run_module1
    run_module1()
elif page == "👩‍🏫 Daftar Kelas":
    from module2 import run_module2
    run_module2()
elif page == "🖥️ Absensi":
    from module3 import run_module3
    run_module3()
elif page == "🌐 Dashboard":
    from module4 import display_summary
    display_summary()

st.markdown("""
    <style>
        .footer {
            text-align: center;
            padding: 10px;
            background-color: #FBBDBA;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        © 2024 Pendaftaran Kelas Online | Semua hak cipta dilindungi.
    </div>
""", unsafe_allow_html=True)
