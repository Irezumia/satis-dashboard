
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Satış Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("satislar.csv", parse_dates=["Tarih"])
    return df

df = load_data()

st.title("📊 Satış Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    sehir = st.multiselect("Şehir", sorted(df["Şehir"].unique()), default=None)
with col2:
    kategori = st.multiselect("Kategori", sorted(df["Kategori"].unique()), default=None)
with col3:
    kanal = st.multiselect("Kanal", sorted(df["Kanal"].unique()), default=None)

f = df.copy()
if sehir:    f = f[f["Şehir"].isin(sehir)]
if kategori: f = f[f["Kategori"].isin(kategori)]
if kanal:    f = f[f["Kanal"].isin(kanal)]

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Toplam Gelir", f"₺{f['Tutar'].sum():,.0f}")
c2.metric("Sipariş", f"{len(f):,}")
c3.metric("AOV", f"₺{f['Tutar'].mean():,.2f}")

# Zaman serisi
st.line_chart(f.set_index("Tarih")["Tutar"].resample("W").sum())

# Kategori & Ürün
st.bar_chart(f.groupby("Kategori")["Tutar"].sum())
top_urun = f.groupby("Ürün")["Tutar"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_urun)
