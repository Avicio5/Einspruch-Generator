import streamlit as st
from fpdf import FPDF
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- PDF LOGIK (Komplett stabilisiert für fpdf2) ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Privates Einspruchsschreiben - Fachportal für Steuerrecht', 0, 1, 'R')

def create_pdf(name, adresse, steuernummer, finanzamt, datum_bescheid, text, betreff):
    pdf = SteuerPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Absender & Empfänger
    pdf.multi_cell(0, 5, f"{name}\n{adresse}")
    pdf.ln(10)
    pdf.multi_cell(0, 5, f"An das\nFinanzamt {finanzamt}")
    pdf.ln(10)
    # Datum & Betreff
    pdf.cell(0, 10, f"Datum: {datetime.now().strftime('%d.%m.%Y')}", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"{betreff} vom {datum_bescheid.strftime('%d.%m.%Y')}", 0, 1)
    pdf.cell(0, 5, f"Steuernummer: {steuernummer}", 0, 1)
    pdf.ln(10)
    # Inhalt
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Sehr geehrte Damen und Herren,\n\n{text}")
    pdf.ln(15)
    pdf.cell(0, 10, "Mit freundlichen Grüßen", 0, 1)
    pdf.cell(0, 10, f"{name}", 0, 1)
    
    # fpdf2 gibt direkt Bytes zurück
    return pdf.output()

# --- APP SETUP ---
st.set_page_config(page_title="Steuer-Einspruch", layout="centered")

# Verbindung sicher aufbauen
conn = None
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

st.title("Einspruch gegen den Steuerbescheid")

# Eingabemaske
u_name = st.text_input("Vollständiger Name")
u_adresse = st.text_area("Anschrift", height=80)
u_snr = st.text_input("Steuernummer")
u_fa = st.text_input("Zuständiges Finanzamt")
fall = st.selectbox("Grund des Einspruchs:", ["Grundsteuer", "Kapitalerträge", "Kryptowährungen", "Fristwahrung"])
u_datum = st.date_input("Datum des Bescheids")

# Texte festlegen (Beispielhaft)
betreff = f"Einspruch im Bereich {fall}"
text_inhalt = "Hiermit lege ich gegen den oben genannten Bescheid Einspruch ein. Eine detaillierte Begründung folgt."

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr:
        # 1. Statistik in Google Tabelle (Downloads)
        if conn:
            try:
                # Neuen Eintrag vorbereiten
                new_row = pd.DataFrame([{"Zeitstempel": datetime.now().strftime("%d.%m.%Y %H:%M"), "Fall": fall}])
                # Bestehende Daten lesen
                existing_data = conn.read(worksheet="Downloads")
                # Zusammenfügen und hochladen
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(worksheet="Downloads", data=updated_df)
            except Exception as e:
                st.info("Statistik-Server kurzzeitig nicht erreichbar, PDF wird trotzdem erstellt.")

        # 2. PDF erstellen & Download anbieten
        try:
            pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text_inhalt, betreff)
            st.download_button(
                label="📥 PDF jetzt herunterladen",
                data=pdf_bytes,
                file_name="Einspruchsschreiben.pdf",
                mime="application/pdf"
            )
            st.success("Fertig! Bitte klicken Sie auf den Button oben zum Speichern.")
        except Exception as e:
            st.error(f"Fehler bei PDF-Erstellung: {e}")
    else:
        st.warning("Bitte füllen Sie Name und Steuernummer aus.")

# --- MISSION ---
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown("""*„Ich arbeite beim Finanzamt und ärgere mich täglich, wie viele Menschen Geld auf der Straße liegen lassen...“*""")

# Footer
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a></div>", unsafe_allow_html=True)

# Admin Bereich
with st.expander("Interner Bereich"):
    pw = st.text_input("PIN", type="password")
    if pw == "1234":
        if conn:
            try:
                data = conn.read(worksheet="Downloads")
                st.metric("Downloads Gesamt", len(data))
                st.dataframe(data.tail(10))
            except Exception as e:
                st.error(f"Tabellenfehler: {e}")
        else:
            st.error("Verbindung zur Tabelle konnte nicht hergestellt werden.")
