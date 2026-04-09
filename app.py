import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. SEO & META SETTINGS ---
st.set_page_config(
    page_title="Steuer-Einspruch Generator | Kostenlose Hilfe & Vorlagen",
    page_icon="⚖️",
    layout="centered"
)

# --- 2. PDF GENERATOR LOGIK (Stabil für fpdf2) ---
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
    
    # Datum & Betreffzeile
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
    
    return pdf.output()

# --- 3. HAUPTSEITE UI ---
st.title("Einspruch gegen den Steuerbescheid")
st.markdown("""
**Helfen Sie sich selbst bei fehlerhaften Bescheiden.** Erstellen Sie in wenigen Schritten ein 
rechtssicheres Dokument zum Ausdrucken und Versenden. Kostenlos und ohne Datenspeicherung.
""")

# Eingabemaske
st.divider()
col1, col2 = st.columns(2)

with col1:
    u_name = st.text_input("Vollständiger Name")
    u_adresse = st.text_area("Anschrift (Straße, PLZ, Ort)", height=100)
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

# Vollständige Texte (Original-Version)
if "Grundsteuer" in fall:
    betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
    text = ("hiermit lege ich Einspruch gegen den Feststellungsbescheid ein. Es bestehen Zweifel an der "
            "rechtmäßigen Ermittlung der Bodenrichtwerte (§ 247 BewG). Um eine Fehlbewertung auszuschließen, "
            "wird um Überprüfung gebeten.")
    tipp = "Hinweis: Ein Einspruch gegen die Grundsteuer hält den Bescheid offen, falls die Bewertungsmethodik später durch den BFH für verfassungswidrig erklärt wird."
elif "Kapitalerträge" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kapitalerträge)"
    text = ("hiermit lege ich Einspruch ein. Die Beschränkung der Verlustverrechnung bei Termingeschäften "
            "wird im Hinblick auf laufende Verfahren (BFH VIII R 11/22) beanstandet. Ich beantrage das Ruhen des Verfahrens.")
    tipp = "Tipp: Die Angabe des BFH-Aktenzeichens (VIII R 11/22) ist hier entscheidend für eine schnelle Bearbeitung."
elif "Krypto" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kryptowerte)"
    text = ("hiermit lege ich Einspruch ein. Die Veräußerungsgeschäfte mit Kryptowerten wurden fälschlicherweise "
            "als steuerpflichtig behandelt, obwohl die einjährige Haltefrist (§ 23 EStG) überschritten war.")
    tipp = "Wichtig: Achten Sie darauf, die Anschaffungs- und Veräußerungsdaten im Zweifel nachweisen zu können."
else:
    betreff = "Einspruch gegen den Steuerbescheid"
    text = "hiermit lege ich fristwahrend Einspruch ein. Eine ausführliche Begründung wird nachgereicht."
    tipp = "Wichtig: Ein fristwahrender Einspruch stoppt die 1-Monats-Frist sofort."

# Vorschau & Download
with st.expander("Vorschau der Begründung"):
    st.write(text)
    st.caption(f"💡 {tipp}")

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr and u_fa and u_adresse:
        try:
            pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
            st.download_button(
                label="📥 Jetzt PDF herunterladen",
                data=pdf_bytes,
                file_name=f"Einspruch_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("Ihr Dokument steht zum Download bereit.")
        except Exception as e:
            st.error(f"Fehler bei der PDF-Erstellung: {e}")
    else:
        st.warning("Bitte füllen Sie alle Felder aus (Name, Anschrift, Steuernummer und Finanzamt).")

# --- 4. SEO RATGEBER & MISSION ---
st.divider()
st.header("Hintergrund & Mission")
st.markdown("""
*„Ich arbeite beim Finanzamt und ärgere mich täglich, wie so viele Menschen Geld auf der Straße liegen lassen, 
weil sie nicht gegen ihre falschen Steuerbescheide vorgehen. Viele Menschen haben immer noch Angst davor, 
sich gegen die Finanzbehörde zu stellen. Dieses Tool wurde entwickelt, um den Menschen dabei zu helfen, 
sich das Geld zurückzuholen, das ihnen auch zusteht und nicht unnötig zu viel zu bezahlen.“*
""")

st.divider()
st.header("Ratgeber: Häufig gestellte Fragen zum Einspruch")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("Wie lange habe ich Zeit?")
    st.write("""
    Die Einspruchsfrist beträgt in der Regel **einen Monat** nach Bekanntgabe des Bescheids. 
    Ausschlaggebend ist das Datum des Poststempels plus drei Tage (Bekanntgabefiktion).
    """)
    
    st.subheader("Was kostet ein Einspruch?")
    st.write("""
    Das Einspruchsverfahren beim Finanzamt ist **grundsätzlich kostenlos**. Es fallen keine 
    staatlichen Gebühren an.
    """)

with col_info2:
    st.subheader("Was ist eine 'Verböserung'?")
    st.write("""
    Das Finanzamt prüft den Fall bei einem Einspruch erneut. Sollte das Ergebnis für Sie 
    schlechter ausfallen, muss das Finanzamt Sie darauf hinweisen und Ihnen die Möglichkeit 
    geben, den Einspruch zurückzunehmen.
    """)

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a> | <a href='#'>Datenschutz</a></div>", unsafe_allow_html=True)
