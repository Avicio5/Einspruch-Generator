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

# Der klassische Eingangstext
st.markdown("""
Erstellen Sie hier Ihr rechtssicheres Schreiben. Alle Vorlagen basieren auf aktueller Rechtsprechung 
und helfen Ihnen, Ihre Rechte gegenüber dem Finanzamt zu wahren. In nur wenigen Klicks haben Sie ihren gesetzeskonformen Einspruch erstellt.
""")

# Kleine Anleitung
st.info("""
**So einfach funktioniert es:**
1. Tragen Sie Ihre Daten und die Steuernummer ein.
2. Wählen Sie den Grund Ihres Einspruchs aus.
3. Klicken Sie auf 'PDF generieren' und speichern Sie das fertige Schreiben.
""")

# Eingabe-Sektion
st.divider()
col1, col2 = st.columns(2)

with col1:
    u_name = st.text_input("Vollständiger Name")
    u_adresse = st.text_area("Ihre Anschrift (Straße, PLZ, Ort)", height=100)
    u_snr = st.text_input("Steuernummer / Identifikationsnummer")

with col2:
    u_fa = st.text_input("Name des Finanzamts")
    fall = st.selectbox("Grund des Einspruchs:", [
        "Grundsteuer: Wertfeststellung (Bodenrichtwert)",
        "Kapitalerträge: Verlustverrechnung § 20 Abs. 6",
        "Kryptowährungen: Haltefrist § 23",
        "Allgemeine Fristwahrung (Begründung folgt)"
    ])
    u_datum = st.date_input("Datum Ihres Bescheids")

# Vollständige Texte
if "Grundsteuer" in fall:
    betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert"
    text = (
        "hiermit lege ich Einspruch gegen den Feststellungsbescheid über den Grundsteuerwert ein. "
        "Es bestehen ernsthafte Zweifel an der rechtmäßigen Ermittlung der zugrunde gelegten Bodenrichtwerte (§ 247 BewG). "
        "Um eine Fehlbewertung meines Grundstücks auszuschließen, wird um eine detaillierte Überprüfung der "
        "Wertfeststellung gebeten. Zudem verweise ich auf die aktuell laufenden verfassungsrechtlichen Prüfungen."
    )
elif "Kapitalerträge" in fall:
    betreff = "Einspruch gegen den Einkommensteuerbescheid (Kapitalerträge)"
    text = (
        "hiermit lege ich Einspruch gegen den oben genannten Bescheid ein. Die steuerliche Behandlung der "
        "Kapitalerträge, insbesondere die Beschränkung der Verlustverrechnung bei Termingeschäften, wird im Hinblick "
        "auf die laufenden Verfahren vor dem Bundesfinanzhof (BFH VIII R 11/22) beanstandet. "
        "Ich beantrage hiermit das Ruhen des Verfahrens bis zu einer endgültigen Entscheidung."
    )
elif "Krypto" in fall:
    betreff = "Einspruch gegen den Einkommensteuerbescheid (Kryptowerte)"
    text = (
        "hiermit lege ich Einspruch gegen den Bescheid ein. Die Veräußerungsgeschäfte mit Kryptowerten wurden "
        "fälschlicherweise als steuerpflichtig behandelt. Gemäß § 23 EStG sind private Veräußerungsgeschäfte steuerfrei, "
        "wenn die Haltefrist von einem Jahr überschritten wurde. Ich bitte um erneute Prüfung der eingereichten "
        "Anschaffungs- und Veräußerungsdaten."
    )
else:
    betreff = "Fristwahrender Einspruch gegen den Steuerbescheid"
    text = (
        "hiermit lege ich fristwahrend Einspruch gegen den oben genannten Bescheid ein. "
        "Zur Vermeidung des Eintritts der Bestandskraft wird dieser Einspruch hiermit form- und fristgerecht erhoben. "
        "Eine ausführliche Begründung der einzelnen Punkte werde ich Ihnen nach Sichtung meiner Unterlagen "
        "in einem gesonderten Schreiben zeitnah nachreichen."
    )

# PDF Button
st.divider()
if st.button("Schreiben als PDF generieren", use_container_width=True):
    if u_name and u_snr and u_fa and u_adresse:
        try:
            pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
            st.download_button(
                label="📥 PDF jetzt herunterladen & speichern",
                data=pdf_bytes,
                file_name=f"Einspruch_{u_name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            st.success("Ihr Schreiben wurde erfolgreich generiert!")
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
    else:
        st.warning("Bitte füllen Sie alle Felder (Name, Anschrift, Steuernummer und Finanzamt) aus.")

# --- 4. MISSIONSTEXT (Neu formatiert) ---
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown(f"""
> *"Ich arbeite beim Finanzamt und ärgere mich täglich darüber, wie viele Menschen Geld auf der Straße liegen lassen, 
> weil sie ihre falschen Steuerbescheide einfach akzeptieren. Viele Menschen haben immer noch Angst davor, 
> sich gegen die Finanzbehörde zu stellen. Doch so ein Steuerbescheid ist kein unumstößliches Gesetz, sondern "nur" ein Verwaltungsakt, der fehleranfällig ist. Dieses Tool soll den Menschen dabei helfen, 
> sich das Geld zurückzuholen, das ihnen rechtmäßig zusteht. Sie sollen nicht unnötig zu viel bezahlen, nur weil der Prozess zu kompliziert wirkt."*
""")

# --- 5. RATGEBER-SEKTION ---
st.divider()
st.header("Ratgeber: Hilfe beim Einspruch gegen das Finanzamt")
st.write("""
Ob Grundsteuer, Kryptowährungen oder Werbungskosten – viele Steuerbescheide in Deutschland sind fehlerhaft. 
Ein Einspruch ist Ihr gutes Recht, um den Bescheid offen zu halten.
""")

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Wann lohnt sich ein Einspruch?")
    st.write("""
    Besonders bei der Grundsteuer und Kryptowährungen gibt es aktuell viele Unklarheiten. 
    Ein Einspruch hält den Fall rechtlich offen und gibt ihnen die Möglichkeit für Korrekturen. Sollten Sie der Meinung sein, dass das Finanzamt etwas falsch berücksichtigt hat, lohnt es sich in den meisten Fällen Einspruch einzulegen.
    """)
    
    st.subheader("Fristen beachten")
    st.write("""
    Ihr Einspruch muss in der Regel spätestens **einen Monat** nach Bekanntgabe des Bescheids beim Finanzamt eingehen. **Wichtig**: Prüfen Sie den Poststempel oder das Datum ihres Bescheides. Rechnen Sie auf dieses Datum **4 Tage** dazu. Dies ist der fiktive Bekanntgabetag ihres Steuerbescheides (sogenannte Bekanntgabefiktion). Bis zu diesem Tag wahren Sie mit ihrem Einspruch die gesetzliche Frist. Danach wird der Bescheid 
    rechtskräftig und ihr Einspruch wird vom Finanzamt nicht mehr berücksichtigt
    """)

with col_b:
    st.subheader("Ist das Verfahren kostenlos?")
    st.write("""
    Ja! Das Einspruchsverfahren beim Finanzamt ist für Sie **vollkommen kostenlos**. 
    Es entstehen keine staatlichen Gebühren.
    """)
    
    st.subheader("Was passiert danach?")
    st.write("""
    Das Finanzamt prüft ihren Fall erneut. Sollte das Ergebnis schlechter ausfallen 
    ('Verböserung'), muss das Amt Sie vorher warnen. Sie können ihren dann immernoch Einspruch zurücknehmen. Es wird nichts geändert und es bleibt bei dem urspünglichen Steuerbescheid. Sie haben also nichts zu verlieren, es kann sich nur für Sie lohnen!
    """)

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Steuer-Portal | <a href='#'>Impressum</a> | <a href='#'>Datenschutz</a></div>", unsafe_allow_html=True)
