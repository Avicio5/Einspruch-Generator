import streamlit as st
from fpdf import FPDF
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- PDF LOGIK (Stabil für moderne fpdf2 Version) ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Privates Einspruchsschreiben - Fachportal für Steuerrecht', 0, 1, 'R')

def create_pdf(name, adresse, steuernummer, finanzamt, datum_bescheid, text, betreff):
    pdf = SteuerPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Absender
    pdf.multi_cell(0, 5, f"{name}\n{adresse}")
    pdf.ln(10)
    # Empfänger
    pdf.multi_cell(0, 5, f"An das\nFinanzamt {finanzamt}")
    pdf.ln(10)
    # Datum & Betreff
    pdf.cell(0, 10, f"Datum: {datetime.now().strftime('%d.%m.%Y')}", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"{betreff} vom {datum_bescheid.strftime('%d.%m.%Y')}", 0, 1)
    pdf.cell(0, 5, f"Steuernummer: {steuernummer}", 0, 1)
    pdf.ln(10)
    # Textinhalt
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Sehr geehrte Damen und Herren,\n\n{text}")
    pdf.ln(15)
    pdf.cell(0, 10, "Mit freundlichen Grüßen", 0, 1)
    pdf.cell(0, 10, f"{name}", 0, 1)
    return pdf.output() # Fix: Kein dest='S' mehr nötig bei fpdf2

# --- UI SETUP ---
st.set_page_config(page_title="Steuer-Einspruch Generator", layout="centered")

# Verbindung zur Tabelle (Optionaler Check, damit App nicht abstürzt)
conn = None
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    conn = None

st.title("Einspruch gegen den Steuerbescheid")
st.markdown("Nutzen Sie dieses Tool, um rechtssichere Einsprüche zu generieren.")

# Eingabemaske
st.divider()
col1, col2 = st.columns(2)
with col1:
    u_name = st.text_input("Vollständiger Name")
    u_adresse = st.text_area("Ihre Anschrift", height=100)
    u_snr = st.text_input("Steuernummer / ID")
with col2:
    u_fa = st.text_input("Zuständiges Finanzamt")
    fall = st.selectbox("Grund des Einspruchs:", [
        "Grundsteuer: Wertfeststellung (Bodenrichtwert)",
        "Kapitalerträge: Verlustverrechnung § 20 Abs. 6",
        "Kryptowährungen: Haltefrist § 23",
        "Allgemeine Fristwahrung"
    ])
    u_datum = st.date_input("Datum des Bescheids")

# Logik für die Texte
if "Grundsteuer" in fall:
    betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
    text = "hiermit lege ich Einspruch gegen den Feststellungsbescheid ein. Es bestehen Zweifel an der rechtmäßigen Ermittlung der Bodenrichtwerte (§ 247 BewG). Um eine Fehlbewertung auszuschließen, wird um Überprüfung gebeten."
elif "Kapitalerträge" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kapitalerträge)"
    text = "hiermit lege ich Einspruch ein. Die Beschränkung der Verlustverrechnung bei Termingeschäften wird im Hinblick auf laufende Verfahren (BFH VIII R 11/22) beanstandet. Ich beantrage das Ruhen des Verfahrens."
elif "Krypto" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kryptowerte)"
    text = "hiermit lege ich Einspruch ein. Die Veräußerungsgeschäfte mit Kryptowerten wurden fälschlicherweise als steuerpflichtig behandelt, obwohl die einjährige Haltefrist (§ 23 EStG) überschritten war. Ich bitte um Prüfung der Anschaffungsdaten."
else:
    betreff = "Einspruch gegen den Steuerbescheid"
    text = "hiermit lege ich fristwahrend Einspruch gegen den oben genannten Bescheid ein. Eine ausführliche Begründung wird nachgereicht."

# Vorschau & PDF Download
st.divider()
with st.expander("Vorschau der Begründung"):
    st.write(text)

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr and u_fa:
        # 1. In Google Tabelle loggen
        if conn:
            try:
                new_row = pd.DataFrame([{"Zeitstempel": datetime.now().strftime("%d.%m.%Y %H:%M"), "Fall": fall}])
                old_data = conn.read(worksheet="Downloads")
                updated_df = pd.concat([old_data, new_row], ignore_index=True)
                conn.update(worksheet="Downloads", data=updated_df)
            except:
                pass # Falls Tabelle fehlschlägt, machen wir trotzdem das PDF
        
        # 2. PDF Erstellung
        pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
        st.download_button("📥 Jetzt PDF herunterladen", data=pdf_bytes, file_name="Einspruch.pdf", mime="application/pdf")
        st.success("PDF wurde erfolgreich erstellt!")
    else:
        st.warning("Bitte füllen Sie alle Felder aus.")

# Mission & Hintergrund
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown("*„Ich arbeite beim Finanzamt und ärgere mich täglich, wie so viele Menschen Geld auf der Straße liegen lassen, weil sie nicht gegen ihre falschen Steuerbescheide vorgehen. Viele Menschen haben immer noch Angst davor sich gegen die Finanzbehörde zustellen. Diese Tool wurde entwickelt, um den Menschen dabei zu helfen sich das Geld zurück zu holen, dass ihnen auch zusteht und nicht unnötig zu viel zu bezahlen.“*")

# FAQ Bereich
st.divider()
st.subheader("Wissenswertes")
c1, c2 = st.columns(2)
with c1:
    st.write("**Frist:** Ein Monat nach Bekanntgabe.")
    st.write("**Kosten:** Das Verfahren beim Finanzamt ist kostenlos.")
with c2:
    st.write("**Verböserung:** Das Amt muss Sie warnen, wenn es teurer werden könnte.")
    st.write("**Rücknahme:** Sie können den Einspruch jederzeit zurückziehen.")

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a> | <a href='#'>Datenschutz</a></div>", unsafe_allow_html=True)

# Admin Bereich
with st.expander("Interner Bereich"):
    pin = st.text_input("PIN", type="password")
    if pin == "1234":
        if conn:
            try:
                data = conn.read(worksheet="Downloads")
                st.metric("Gesamte Downloads", len(data))
                st.dataframe(data.tail(10))
            except Exception as e:
                st.error(f"Tabellen-Fehler: {e}")
