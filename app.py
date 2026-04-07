import streamlit as st
from fpdf import FPDF
from datetime import date

# --- PDF LOGIK (Bleibt stabil) ---
class SteuerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Privates Einspruchsschreiben - Erstellt via Steuer-Portal', 0, 1, 'R')

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
st.set_page_config(page_title="Steuer-Einspruch & Analyse | Fachportal", layout="centered")

# Header & Intro (SEO & Vertrauen)
st.title("Einspruch gegen den Steuerbescheid")
st.markdown("""
Jedes Jahr werden in Deutschland Millionen von Steuerbescheiden erlassen – und ein signifikanter Teil davon enthält Fehler. 
Ob veraltete Bodenrichtwerte bei der Grundsteuer oder nicht anerkannte Werbungskosten: Ein Einspruch ist oft der einzige Weg, 
um eine Korrektur zu erwirken. 

Dieses Portal bietet Ihnen fundierte Informationen zu aktuellen Rechtsentwicklungen und hilft Ihnen, 
formgerechte Schreiben für Ihr Finanzamt zu erstellen. Mit nur wenigen Klicks hilft Ihnen der Einspruchs-Generator dabei erfolgreich einen Einspruch bei Ihrem Finanzamt einzulegen.
""")

# Das Tool - eingebettet in die Seite
st.divider()
st.subheader("Digitaler Assistent für Einspruchsschreiben")
st.caption("Nutzen Sie unsere Vorlagen, die auf gängigen Fallkonstellationen der Finanzverwaltung basieren.")

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

# Logik-Bereich (Hier fließen deine Insider-Infos ein)
if "Grundsteuer" in fall:
    betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
    text = "hiermit lege ich Einspruch gegen den Feststellungsbescheid ein. Es bestehen Zweifel an der rechtmäßigen Ermittlung der Bodenrichtwerte (§ 247 BewG). Um eine Fehlbewertung auszuschließen, wird um Überprüfung gebeten."
    hinweis = "Insider-Tipp: Bei der Grundsteuer reicht oft ein Verweis auf die Verfassungsmäßigkeit der Bewertung aus, um das Verfahren offen zu halten."
elif "Kapitalerträge" in fall:
    betreff = "Einspruch gegen ESt-Bescheid (Kapitalerträge)"
    text = "hiermit lege ich Einspruch ein. Die Beschränkung der Verlustverrechnung bei Termingeschäften wird im Hinblick auf laufende Verfahren (BFH VIII R 11/22) beanstandet. Ich beantrage das Ruhen des Verfahrens."
    hinweis = "Wichtig: Nennen Sie immer das konkrete BFH-Aktenzeichen, damit der Sachbearbeiter den Fall sofort zuordnen kann."
else:
    betreff = "Einspruch gegen den Steuerbescheid"
    text = "hiermit lege ich fristwahrend Einspruch ein. Eine ausführliche Begründung wird nachgereicht."
    hinweis = "Info: Ein fristwahrender Einspruch stoppt die 1-Monats-Frist, auch wenn Sie noch keine Details bereit haben."

with st.expander("Vorschau der Begründung & fachlicher Hintergrund"):
    st.write(text)
    st.divider()
    st.caption(hinweis) # Hier ist das Insiderwissen subtil verpackt

if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr and u_fa:
        pdf_out = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
        st.download_button("Datei jetzt speichern", data=pdf_out, file_name="Einspruchsschreiben.pdf", mime="application/pdf")
    else:
        st.warning("Bitte ergänzen Sie die Basis-Daten für ein vollständiges PDF.")

# SEO & Informationsteil (Die Prosa)
st.divider()
st.subheader("Häufig gestellte Fragen zum Einspruch")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    **Wie lange habe ich Zeit?** Die Einspruchsfrist beträgt in der Regel einen Monat nach Bekanntgabe des Bescheids. 
    Es ist ratsam, den Poststempel oder das Datum der elektronischen Bereitstellung (ELSTER) zu prüfen.
    
    **Was kostet ein Einspruch?** Das außergerichtliche Rechtsbehelfsverfahren (Einspruchsverfahren) beim Finanzamt ist grundsätzlich kostenlos. 
    Es fallen keine Gebühren an, es sei denn, Sie beauftragen einen Steuerberater.
    """)

with col_info2:
    st.markdown("""
    **Was passiert nach dem Einspruch?** Das Finanzamt prüft den Fall erneut in vollem Umfang. Dies kann zu einer Abhilfe (Erfolg) 
    oder einer Einspruchsentscheidung führen. Achtung: Eine 'Verböserung' ist theoretisch möglich.
    
    **Kann ich den Einspruch zurücknehmen?** Ja, ein Einspruch kann jederzeit zurückgenommen werden, solange noch keine endgültige 
    Entscheidung getroffen wurde.
    """)

# Subtiles Footer-Statement
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Dieses Projekt wird von Experten aus dem Bereich der Finanzverwaltung begleitet, 
    um Bürgern einen einfachen Zugang zu rechtssicheren Vorlagen zu ermöglichen. <br>
    © 2026 Steuer-Portal | <a href='#'>Impressum</a> | <a href='#'>Datenschutz</a>
</div>
""", unsafe_allow_html=True)
  
