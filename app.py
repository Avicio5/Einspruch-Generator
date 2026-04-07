import streamlit as st
from fpdf import FPDF
from datetime import date

# --- PDF LOGIK ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'OFFIZIELLES EINSPRUCHSSCHREIBEN', 0, 1, 'R')
        self.ln(5)

def create_pdf(name, adresse, steuernummer, finanzamt, datum_bescheid, text, betreff):
    pdf = SteuerPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 5, f"{name}\n{adresse}")
    pdf.ln(10)
    pdf.multi_cell(0, 5, f"An das\nFinanzamt {finanzamt}")
    pdf.ln(10)
    pdf.cell(0, 10, f"Datum: {date.today().strftime('%d.%m.%Y')}", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"{betreff} vom {datum_bescheid.strftime('%d.%m.%Y')}", 0, 1)
    pdf.cell(0, 5, f"Steuernummer: {steuernummer}", 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Sehr geehrte Damen und Herren,\n\n{text}")
    pdf.ln(10)
    pdf.cell(0, 10, "Mit freundlichen Grüßen", 0, 1)
    pdf.cell(0, 10, f"{name}", 0, 1)
    return bytes(pdf.output())

# --- UI DESIGN ---
st.set_page_config(page_title="Tax-Expert | Insider-Tools", layout="wide")

# Sidebar für Seriosität
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2821/2821637.png", width=100)
    st.title("Tax-Expert Insider")
    st.success("✅ Verifiziertes Insider-Wissen")
    st.markdown("""
    **Warum uns vertrauen?**
    * Entwicklung durch Experten der Finanzverwaltung.
    * Nutzung aktueller BFH-Rechtsprechung.
    * 100% DSGVO-konform (keine Datenspeicherung).
    """)
    st.divider()
    with st.expander("Rechtliches & Impressum"):
        st.caption("Betreiber: [Dein Name/Pseudonym]")
        st.caption("Kontakt: [Deine E-Mail]")
        st.caption("Keine Steuerberatung gemäß RDG.")

# Hauptbereich
st.title("Steuerbescheid prüfen & Einspruch erstellen")
st.write("Wählen Sie Ihren Fall aus und lassen Sie die Logik eines Finanzbeamten für sich arbeiten.")

tab1, tab2 = st.tabs(["📑 Einspruch-Generator", "🔍 Hilfe & Anleitung"])

with tab1:
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("1. Basis-Daten")
        u_name = st.text_input("Name")
        u_adresse = st.text_area("Anschrift")
        u_snr = st.text_input("Steuernummer")
        u_fa = st.text_input("Finanzamt")
        
    with col_b:
        st.subheader("2. Fall-Auswahl")
        fall = st.selectbox("Was ist passiert?", [
            "Grundsteuerwertbescheid (Fehlerhafter Bodenrichtwert/Fläche)",
            "Krypto-Verluste (Nichtanerkennung durch FA)",
            "Werbungskosten (Arbeitszimmer/Home-Office)",
            "Fristwahrung (Begründung folgt später)"
        ])
        u_datum = st.date_input("Datum des Bescheids")
        
        # Insider-Logik Texte
        if "Grundsteuer" in fall:
            betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
            text = "hiermit lege ich Einspruch gegen den Feststellungsbescheid ein. Die angesetzten Bodenrichtwerte entsprechen nicht den tatsächlichen Gegebenheiten (§ 247 BewG). Zudem wird die Verfassungsmäßigkeit der Bewertungsmethodik angezweifelt."
        elif "Krypto" in fall:
            betreff = "Einspruch gegen ESt-Bescheid (Kryptowerte)"
            text = "hiermit lege ich Einspruch ein. Die Veräußerungsgeschäfte mit Kryptowerten wurden fälschlicherweise als steuerpflichtig behandelt, obwohl die einjährige Haltefrist (§ 23 EStG) überschritten war."
        else:
            betreff = "Einspruch gegen den Einkommensteuerbescheid"
            text = "hiermit lege ich zur Fristwahrung Einspruch ein. Eine detaillierte Begründung wird nach Sichtung aller Unterlagen nachgereicht."

        st.info(f"**Vorschau Begründung:**\n\n{text}")

    if st.button("📄 Rechtssicheres PDF generieren", use_container_width=True):
        if u_name and u_snr:
            pdf_out = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
            st.download_button("Download Starten", data=pdf_out, file_name="Einspruch.pdf", mime="application/pdf")
        else:
            st.error("Bitte füllen Sie die Pflichtfelder aus.")

with tab2:
    st.subheader("So gehen Sie vor:")
    st.write("1. Daten aus Ihrem Steuerbescheid eingeben.")
    st.write("2. PDF herunterladen und ausdrucken.")
    st.write("3. Per Post oder ELSTER (als Anhang) an Ihr Finanzamt senden.")
    st.warning("⚠️ Wichtig: Die Einspruchsfrist beträgt genau einen Monat nach Erhalt des Bescheids!")
