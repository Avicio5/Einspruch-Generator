import streamlit as st
from fpdf import FPDF
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- PDF GENERATOR ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Privates Einspruchsschreiben - Fachportal für Steuerrecht', 0, 1, 'R')

def create_pdf(name, adresse, steuernummer, finanzamt, datum_bescheid, text, betreff):
    pdf = SteuerPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 5, f"{name}\n{adresse}")
    pdf.ln(10)
    pdf.multi_cell(0, 5, f"An das\nFinanzamt {finanzamt}")
    pdf.ln(10)
    pdf.cell(0, 10, f"Datum: {datetime.now().strftime('%d.%m.%Y')}", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"{betreff} vom {datum_bescheid.strftime('%d.%m.%Y')}", 0, 1)
    pdf.cell(0, 5, f"Steuernummer: {steuernummer}", 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Sehr geehrte Damen und Herren,\n\n{text}")
    pdf.ln(15)
    pdf.cell(0, 10, "Mit freundlichen Grüßen", 0, 1)
    pdf.cell(0, 10, f"{name}", 0, 1)
    return bytes(pdf.output())

# --- UI SETUP ---
st.set_page_config(page_title="Steuer-Einspruch | Fachportal", layout="centered")

# VERSUCH DER VERBINDUNG
conn = None
connection_error = None
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    connection_error = str(e)

st.title("Einspruch gegen den Steuerbescheid")
st.markdown("Helfen Sie sich selbst bei fehlerhaften Steuerbescheiden.")

# Formular
st.divider()
col_left, col_right = st.columns(2)
with col_left:
    u_name = st.text_input("Name")
    u_adresse = st.text_area("Anschrift", height=100)
    u_snr = st.text_input("Steuernummer / ID")
with col_right:
    u_fa = st.text_input("Zuständiges Finanzamt")
    fall = st.selectbox("Grund:", ["Grundsteuer: Wertfeststellung (Bodenrichtwert)", "Allgemeine Fristwahrung"])
    u_datum = st.date_input("Datum des Bescheids")

# Texte festlegen
betreff = "Einspruch gegen Steuerbescheid"
text = "Hiermit lege ich Einspruch ein..."

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr:
        # Versuch in Tabelle zu schreiben
        if conn:
            try:
                new_row = pd.DataFrame([{"Zeitstempel": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Fall": fall}])
                existing_data = conn.read(worksheet="Downloads")
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(worksheet="Downloads", data=updated_df)
            except Exception as e:
                st.error(f"Fehler beim Speichern in Tabelle: {e}")
        
        pdf_out = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
        st.download_button("Datei jetzt speichern", data=pdf_out, file_name="Einspruch.pdf")
    else:
        st.warning("Bitte Namen und Steuernummer ausfüllen.")

# Hintergrund & Mission
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown("""*„Ich arbeite beim Finanzamt und ärgere mich täglich, wie so viele Menschen Geld auf der Straße liegen lassen...“*""")

# FAQ & Impressum (gekürzt für Übersicht)
st.divider()
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a></div>", unsafe_allow_html=True)

# --- INTERNER BEREICH MIT FEHLERSUCHE ---
st.divider()
with st.expander("Interner Bereich (Admin)"):
    pw = st.text_input("PIN eingeben (Standard: 1234)", type="password")
    
    if pw == "1234":
        st.success("PIN korrekt!")
        if conn:
            try:
                stats = conn.read(worksheet="Downloads")
                st.metric("Gesamte Downloads", len(stats))
                st.dataframe(stats)
            except Exception as e:
                st.error(f"Verbindung zur Tabelle fehlgeschlagen. Fehler: {e}")
                st.info("Hinweis: Prüfe, ob das Tabellenblatt wirklich 'Downloads' heißt.")
        else:
            st.error("Keine Google-Sheets Verbindung konfiguriert.")
            if connection_error:
                st.code(connection_error)
            st.info("Checke deine 'Secrets' im Streamlit Dashboard!")
    elif pw != "":
        st.error("PIN falsch.")
