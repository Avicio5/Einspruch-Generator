import streamlit as st
from fpdf import FPDF
from datetime import date

# --- PDF GENERATOR KLASSE ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Privates Einspruchsschreiben', 0, 1, 'R')
        self.ln(10)

# Funktion zur PDF-Erstellung
def create_pdf(name, adresse, steuernummer, finanzamt, datum_bescheid, text):
    pdf = SteuerPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Absender & Empfänger
    pdf.multi_cell(0, 5, f"{name}\n{adresse}")
    pdf.ln(15)
    pdf.multi_cell(0, 5, f"An das\nFinanzamt {finanzamt}\n(Zuständige Stelle für Einkommensteuer)")
    pdf.ln(10)
    
    # Datum & Betreff
    pdf.cell(0, 10, f"Datum: {date.today().strftime('%d.%m.%Y')}", 0, 1, 'R')
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"Einspruch gegen den Einkommensteuerbescheid vom {datum_bescheid.strftime('%d.%m.%Y')}", 0, 1)
    pdf.cell(0, 5, f"Steuernummer: {steuernummer}", 0, 1)
    pdf.ln(10)
    
    # Textinhalt
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Sehr geehrte Damen und Herren,\n\n{text}")
    pdf.ln(15)
    pdf.cell(0, 10, "Mit freundlichen Grüßen", 0, 1)
    pdf.ln(5)
    pdf.cell(0, 10, f"{name}", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Tax-Insider.de | Einspruch-Generator", page_icon="⚖️")

# Styling & Insider-Header
st.title("⚖️ Tax-Insider Einspruch-Generator")
st.info("💡 **Insider-Vorteil:** Dieses Tool nutzt die offizielle Logik der Finanzverwaltung, um Einsprüche so zu formulieren, dass sie im Amt direkt korrekt zugeordnet werden können.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Deine Daten")
    u_name = st.text_input("Vollständiger Name", placeholder="Max Mustermann")
    u_adresse = st.text_area("Deine Anschrift", placeholder="Musterstraße 1, 12345 Stadt")
    u_snr = st.text_input("Steuernummer / ID-Nr.")
    u_fa = st.text_input("Zuständiges Finanzamt")

with col2:
    st.header("2. Der Fall")
    fall = st.selectbox("Grund des Einspruchs:", [
        "Verlustverrechnung Termingeschäfte (§ 20 Abs. 6 EStG)",
        "Krypto: Haltefrist nicht berücksichtigt",
        "Günstigerprüfung vergessen",
        "Sonstiger Grund / Fristwahrung"
    ])
    u_bescheid_datum = st.date_input("Datum des Bescheids")

# Logik für die Begründungstexte
begruendung = ""
if "Verlustverrechnung" in fall:
    begruendung = "hiermit lege ich Einspruch gegen den oben genannten Bescheid ein.\n\nBegründung: Die Verlustverrechnungsbeschränkung für Termingeschäfte ist verfassungswidrig. Ich beantrage das Ruhen des Verfahrens im Hinblick auf das BFH-Verfahren (Az. VIII R 11/22)."
elif "Krypto" in fall:
    begruendung = "hiermit lege ich Einspruch ein, da die Haltefrist von einem Jahr gemäß § 23 EStG bei den veräußerten Krypto-Werten nicht korrekt berücksichtigt wurde. Ich bitte um Prüfung der Anschaffungsdaten."
elif "Günstigerprüfung" in fall:
    begruendung = "hiermit lege ich Einspruch ein und beantrage die Günstigerprüfung für Kapitalerträge gemäß § 32d Abs. 6 EStG, da mein persönlicher Steuersatz unter 25% liegt."
else:
    begruendung = "hiermit lege ich Einspruch ein. Die detaillierte Begründung folgt in einem gesonderten Schreiben zur Fristwahrung."

st.write("---")
st.header("3. Vorschau & Download")
st.text_area("Vorschau des Schreibens:", begruendung, height=150)

# PDF Button
if st.button("Download Einspruch als PDF"):
    if u_name and u_snr and u_fa:
        pdf_data = create_pdf(u_name, u_adresse, u_snr, u_fa, u_bescheid_datum, begruendung)
        st.download_button(
            label="📄 Jetzt PDF herunterladen",
            data=pdf_data,
            file_name=f"Einspruch_{u_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("⚠️ Bitte fülle Name, Steuernummer und Finanzamt aus, um das PDF zu erstellen.")

st.sidebar.markdown("---")
st.sidebar.subheader("Warum diesem Tool vertrauen?")
st.sidebar.write("✅ Von Finanzbeamten entwickelt")
st.sidebar.write("✅ Aktuelle BFH-Aktenzeichen")
st.sidebar.write("✅ Rechtssichere Formulierungen")
st.sidebar.markdown("---")
st.sidebar.caption("Hinweis: Dies ist keine Steuerberatung, sondern eine Ausfüllhilfe.")
