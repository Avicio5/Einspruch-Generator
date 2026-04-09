import streamlit as st
from fpdf import FPDF
from datetime import date

# --- PDF LOGIK ---
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
    pdf.cell(0, 10, f"Datum: {date.today().strftime('%d.%m.%Y')}", 0, 1, 'R')
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

# --- UI DESIGN ---
st.set_page_config(page_title="Steuer-Einspruch | Fachportal & Analyse", layout="centered")

# Hero Section
st.title("Einspruch gegen den Steuerbescheid")
st.markdown("""
Jedes Jahr werden Millionen von Steuerbescheiden erlassen – viele davon sind fehlerhaft. 
Ob veraltete Bodenrichtwerte oder nicht anerkannte Werbungskosten: Ein Einspruch ist oft der einzige Weg zur Korrektur.
Wir helfen Ihnen, rechtssichere Schreiben basierend auf aktueller Rechtsprechung zu erstellen.
""")

# Das Tool
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    u_name = st.text_input("Name")
    u_adresse = st.text_area("Anschrift", height=100)
    u_snr = st.text_input("Steuernummer / ID")

with col_right:
    u_fa = st.text_input("Zuständiges Finanzamt")
    fall = st.selectbox("Grund des Einspruchs:", [
        "Grundsteuer: Wertfeststellung (Bodenrichtwert)",
        "Kapitalerträge: Verlustverrechnung § 20 Abs. 6",
        "Kryptowährungen: Haltefrist § 23",
        "Allgemeine Fristwahrung"
    ])
    u_datum = st.date_input("Datum des Bescheids")

# Begründungs-Logik
if "Grundsteuer" in fall:
    betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
    text = "hiermit lege ich Einspruch gegen den Feststellungsbescheid ein. Es bestehen Zweifel an der rechtmäßigen Ermittlung der Bodenrichtwerte (§ 247 BewG). Um eine Fehlbewertung auszuschließen, wird um Überprüfung gebeten."
    tipp = "Hinweis: Ein Einspruch gegen die Grundsteuer hält den Bescheid offen, falls die Bewertungsmethodik später durch den BFH für verfassungswidrig erklärt wird."
elif "Kapitalerträge" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kapitalerträge)"
    text = "hiermit lege ich Einspruch ein. Die Beschränkung der Verlustverrechnung bei Termingeschäften wird im Hinblick auf laufende Verfahren (BFH VIII R 11/22) beanstandet. Ich beantrage das Ruhen des Verfahrens."
    tipp = "Tipp: Die Angabe des BFH-Aktenzeichens (VIII R 11/22) ist hier entscheidend für eine schnelle Bearbeitung."
else:
    betreff = "Einspruch gegen den Steuerbescheid"
    text = "hiermit lege ich fristwahrend Einspruch ein. Eine ausführliche Begründung wird nachgereicht."
    tipp = "Wichtig: Ein fristwahrender Einspruch stoppt die 1-Monats-Frist sofort."

with st.expander("Vorschau der rechtlichen Begründung"):
    st.write(text)
    st.caption(f"💡 {tipp}")

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr and u_fa:
        pdf_out = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
        st.download_button("Datei jetzt speichern", data=pdf_out, file_name="Einspruchsschreiben.pdf", mime="application/pdf")
    else:
        st.warning("Bitte ergänzen Sie die Basis-Daten für ein vollständiges PDF.")

# Hintergrund & Mission
st.divider()
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Hintergrund & Mission")
with col2:
    st.markdown(f"""
    *„Als Mitarbeiter in der Finanzverwaltung ärgere ich mich täglich darüber, wie viele Menschen Geld auf der Straße liegen lassen, weil sie fehlerhafte Steuerbescheide einfach akzeptieren.“*
    
    Viele Bürger haben Hemmungen oder schlichtweg Angst davor, sich gegen eine Behörde zu stellen. Doch ein Steuerbescheid ist kein unumstößliches Gesetz, sondern ein Verwaltungsakt, der fehleranfällig ist. 
    
    Dieses Tool wurde entwickelt, um diese Hürde zu senken. Mein Ziel ist es, Ihnen dabei zu helfen, sich das Geld zurückzuholen, das Ihnen rechtmäßig zusteht. Sie sollen nicht unnötig viel bezahlen, nur weil der Prozess kompliziert wirkt.
    """)

# WISSENSWERTES ZUM RECHTSBEHELF (Wiederhergestellt auf ausführliche Version)
st.divider()
st.subheader("Häufig gestellte Fragen zum Einspruch")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    **Wie lange habe ich Zeit?** Die Einspruchsfrist beträgt in der Regel einen Monat nach Bekanntgabe des Bescheids. 
    Es ist ratsam, den Poststempel oder das Datum der elektronischen Bereitstellung (ELSTER) zu prüfen.
    
    **Was kostet ein Einspruch?** Das außergerichtliche Rechtsbehelfsverfahren beim Finanzamt ist grundsätzlich kostenlos. 
    Es fallen keine Gebühren an, es sei denn, Sie beauftragen einen Steuerberater.
    """)

with col_info2:
    st.markdown("""
    **Was passiert nach dem Einspruch?** Das Finanzamt prüft den Fall erneut in vollem Umfang. Dies kann zu einer Abhilfe (Erfolg) 
    oder einer Einspruchsentscheidung führen. Achtung: Eine 'Verböserung' ist theoretisch möglich.
    
    **Kann ich den Einspruch zurücknehmen?** Ja, ein Einspruch kann jederzeit zurückgenommen werden, solange noch keine endgültige 
    Entscheidung getroffen wurde.
    """)

# FOOTER (Wiederhergestellt auf exakte Vorversion)
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Dieses Projekt wird von Experten aus dem Bereich der Finanzverwaltung begleitet, 
    um Bürgern einen einfachen Zugang zu rechtssicheren Vorlagen zu ermöglichen. <br>
    © 2026 Steuer-Portal | <a href='#'>Impressum</a> | <a href='#'>Datenschutz</a>
</div>
""", unsafe_allow_html=True)
# --- SEO TEXTE (Unter dem Generator einfügen) ---
st.divider()
st.header("Ratgeber: Einspruch gegen den Steuerbescheid")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Wann lohnt sich ein Einspruch?")
    st.write("""
    Besonders bei der **Grundsteuer** und **Kryptowährungen** gibt es aktuell viele Unklarheiten. 
    Häufig werden Bodenrichtwerte falsch übernommen oder Haltefristen von über einem Jahr nicht 
    korrekt berücksichtigt. Ein Einspruch ist Ihr gutes Recht, um den Bescheid offen zu halten, 
    bis die Rechtslage endgültig geklärt ist.
    """)

with col_b:
    st.subheader("Fristen und Kosten")
    st.write("""
    Die Einspruchsfrist beträgt in der Regel **einen Monat** nach Erhalt des Bescheids. 
    Wichtig zu wissen: Das Einspruchsverfahren beim Finanzamt ist für Sie **vollkommen kostenlos**. 
    Es entstehen keine Gebühren, solange Sie keinen Steuerberater oder Anwalt hinzuziehen.
    """)

st.subheader("Schritt-für-Schritt Anleitung")
st.markdown("""
1. **Daten eingeben:** Tragen Sie Ihren Namen, Anschrift und Steuernummer ein.
2. **Grund wählen:** Wählen Sie den passenden Fall (z.B. Grundsteuer oder Krypto).
3. **PDF generieren:** Laden Sie das fertige Schreiben herunter.
4. **Versenden:** Drucken Sie das Dokument aus und schicken Sie es per Post oder Fax an Ihr Finanzamt.
""")
