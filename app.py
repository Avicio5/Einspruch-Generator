import streamlit as st
from fpdf import FPDF
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- PDF LOGIK (GEFIXT) ---
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
    
    # WICHTIG: fpdf2 gibt mit .output() direkt Bytes zurück
    return pdf.output()

# --- APP SETUP ---
st.set_page_config(page_title="Steuer-Einspruch", layout="centered")

# Verbindung versuchen (ohne die ganze App zu killen)
conn = None
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

st.title("Einspruch gegen den Steuerbescheid")
st.write("Erstellen Sie hier Ihr rechtssicheres Schreiben.")

# Eingabemaske
with st.container():
    u_name = st.text_input("Name")
    u_adresse = st.text_area("Anschrift", height=80)
    u_snr = st.text_input("Steuernummer")
    u_fa = st.text_input("Finanzamt")
    fall = st.selectbox("Grund:", ["Grundsteuer", "Kapitalerträge", "Krypto", "Fristwahrung"])
    u_datum = st.date_input("Datum des Bescheids")

# Texte (Deine bewährten Texte)
betreff = f"Einspruch gegen {fall}"
text_inhalt = "Hiermit lege ich Einspruch ein..." 

if st.button("PDF generieren & speichern"):
    if u_name and u_snr:
        # 1. In Tabelle schreiben (wenn Verbindung da ist)
        if conn:
            try:
                new_data = pd.DataFrame([{"Zeitstempel": datetime.now().strftime("%d.%m.%Y %H:%M"), "Fall": fall}])
                old_data = conn.read(worksheet="Downloads")
                updated = pd.concat([old_data, new_data], ignore_index=True)
                conn.update(worksheet="Downloads", data=updated)
            except Exception:
                pass # Falls Tabelle zickt, machen wir trotzdem das PDF!

        # 2. PDF erstellen
        try:
            pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text_inhalt, betreff)
            st.download_button("PDF jetzt herunterladen", data=pdf_bytes, file_name="Einspruch.pdf", mime="application/pdf")
            st.success("Erfolgreich! Klicken Sie oben auf den Button zum Speichern.")
        except Exception as e:
            st.error(f"PDF-Fehler: {e}")
    else:
        st.warning("Bitte Namen und Steuernummer angeben.")

# --- MISSION & WISSENSWERTES ---
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown("""*„Ich arbeite beim Finanzamt und ärgere mich täglich, wie so viele Menschen Geld auf der Straße liegen lassen...“*""")

st.divider()
st.subheader("Wissenswertes")
st.write("Ein Einspruch ist kostenlos und muss innerhalb eines Monats erfolgen.")

# Footer
st.markdown("<div style='text-align:center; color:gray; font-size:0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a></div>", unsafe_allow_html=True)

# Admin Bereich
with st.expander("Interner Bereich"):
    pw = st.text_input("PIN", type="password")
    if pw == "1234":
        if conn:
            try:
                data = conn.read(worksheet="Downloads")
                st.metric("Downloads gesamt", len(data))
                st.table(data.tail(5))
            except Exception as e:
                st.error(f"Tabellen-Fehler: {e}. Prüfe, ob das Blatt 'Downloads' heißt.")
        else:
            st.error("Verbindung zur Tabelle fehlt (Secrets prüfen!).")
