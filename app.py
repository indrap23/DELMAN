import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.title('Input Data Nilai berdasarkan Provinsi dan Sektor')

# Fungsi untuk membaca file pickle
def load_data(file):
    with open(file, 'rb') as f:
        data = joblib.load(f)
    return data

# Memuat data dari file pickle hanya sekali dan menyimpannya di session state
if 'matriks_isi' not in st.session_state:
    st.session_state.matriks_isi = load_data("df_matriks.pkl")

# Mengambil DataFrame dari session state
matriks_isi = st.session_state.matriks_isi

inverse_matrix = load_data('inverse_matrix.pkl')
MTK = load_data('MTK.pkl')
MUG = load_data('MUG.pkl')

# Dropdown untuk memilih provinsi dan sektor
provinsi = st.selectbox('Pilih Provinsi', matriks_isi.index)
sektor = st.selectbox('Pilih Sektor', matriks_isi.columns)

# Input untuk nilai baru
nilai_baru = st.number_input('Masukkan Nilai Baru (dalam juta Rupiah)', value=float(matriks_isi.loc[provinsi, sektor]))

# Tombol untuk memperbarui nilai
if st.button('Add'):
    st.session_state.matriks_isi.loc[provinsi, sektor] += nilai_baru
    st.success(f'Nilai untuk provinsi {provinsi} dan sektor {sektor} berhasil ditambahkan dengan {nilai_baru}. Nilai sekarang adalah {matriks_isi.loc[provinsi, sektor]}')

# Tombol untuk mengembalikan nilai matriks_isi ke 0
if st.button('Clear'):
    st.session_state.matriks_isi = pd.DataFrame(0, index=matriks_isi.index, columns=matriks_isi.columns)
    st.success('Nilai matriks_isi berhasil direset ke 0.')
    st.experimental_rerun()

# Menambahkan total per baris dan per kolom pada matriks_isi
matriks_isi_with_totals = matriks_isi.copy()
matriks_isi_with_totals['Total Per Provinsi'] = matriks_isi.sum(axis=1)
matriks_isi_with_totals.loc['Total Per Sektor'] = matriks_isi_with_totals.sum()

# Menampilkan DataFrame yang telah diperbarui
st.write('Dataframe yang diperbarui:')
st.dataframe(matriks_isi_with_totals)



# Tombol untuk melakukan perhitungan
if st.button('Hitung'):
    matriks = matriks_isi.to_numpy()  # Mengubah DataFrame menjadi numpy array
    matriks_pakai = matriks.reshape(578,)  # Mengubah matriks menjadi satu dimensi
    hasil_1 = np.dot(inverse_matrix, matriks_pakai).reshape(34, 17)  # Mengubah hasil_1 menjadi matrik 34x17
    hasil_2 = np.dot(MUG, np.dot(inverse_matrix, matriks_pakai)).reshape(34, 17)  # Mengubah hasil_2 menjadi matrik 34x17
    hasil_3 = np.dot(MTK, np.dot(inverse_matrix, matriks_pakai)).reshape(34, 17)  # Mengubah hasil_3 menjadi matrik 34x17
    
    hasil_df_1 = pd.DataFrame(hasil_1, index=matriks_isi.index, columns=matriks_isi.columns)
    hasil_df_2 = pd.DataFrame(hasil_2, index=matriks_isi.index, columns=matriks_isi.columns)
    hasil_df_3 = pd.DataFrame(hasil_3, index=matriks_isi.index, columns=matriks_isi.columns)
    
    # Menambahkan total per baris dan per kolom pada hasil_1, hasil_2, dan hasil_3
    hasil_df_1_with_totals = hasil_df_1.copy()
    hasil_df_1_with_totals['Total Per Provinsi'] = hasil_df_1.sum(axis=1)
    hasil_df_1_with_totals.loc['Total Per Sektor'] = hasil_df_1_with_totals.sum()
    
    hasil_df_2_with_totals = hasil_df_2.copy()
    hasil_df_2_with_totals['Total Per Provinsi'] = hasil_df_2.sum(axis=1)
    hasil_df_2_with_totals.loc['Total Per Sektor'] = hasil_df_2_with_totals.sum()
    
    hasil_df_3_with_totals = hasil_df_3.copy()
    hasil_df_3_with_totals['Total Per Provinsi'] = hasil_df_3.sum(axis=1)
    hasil_df_3_with_totals.loc['Total Per Sektor'] = hasil_df_3_with_totals.sum()
    
    st.write("Dampak terhadap OUTPUT (Economic Impact/multiplayer) - IDR Juta")
    st.dataframe(hasil_df_1_with_totals)
    st.write("Dampak terhadap PENDAPATAN (Upah Tenaga Kerja) - IDR Juta")
    st.dataframe(hasil_df_2_with_totals)
    st.write("Dampak terhadap TENAGA KERJA (jiwa orang)")
    st.dataframe(hasil_df_3_with_totals)

