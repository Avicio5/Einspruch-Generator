import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. SEO & META SETTINGS ---
st.set_page_config(
    page_title="Steuer-Einspruch-Generator | Rechtssicher & Kostenlos",
    page_icon="⚖️",
    layout="centered"
)

# --- 2. SAUBERES CSS (Nur Branding ausblenden, Layout intakt lassen) ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 3. PDF GENERATOR LOGIK ---
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


# --- 4. HEADER BEREICH ---
st.title("⚖️ Dein Einspruch ans Finanzamt")
st.markdown("""
    ### In 3 Minuten rechtssicher erstellt.
    **Kostenlos. Ohne Registrierung. Direkt als PDF zum Ausdrucken.**
""")

st.warning("⚠️ **Achtung:** Die Einspruchsfrist beträgt in der Regel nur **einen Monat** nach Erhalt des Steuerbescheids. Handle jetzt!")

# Prozessübersicht
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("📝 **1. Daten eingeben**")
    st.caption("Einfach & verständlich")
with col2:
    st.markdown("⚙️ **2. PDF erstellen**")
    st.caption("Automatisch generiert")
with col3:
    st.markdown("🖨️ **3. Abschicken**")
    st.caption("Unterschreiben & Post")

st.divider()

st.info("🔒 **100% Datenschutz:** Deine Daten werden lokal in deinem Browser verarbeitet und zu keinem Zeitpunkt auf Servern gespeichert.")


# --- 5. DAS FORMULAR ---
tab1, tab2, tab3 = st.tabs(["👤 Deine Daten", "🏢 Finanzamt & Bescheid", "💡 Begründung"])

with tab1:
    st.subheader("Persönliche Informationen")
    u_name = st.text_input("Vollständiger Name", placeholder="Max Mustermann")
    u_adresse = st.text_area("Ihre Anschrift", placeholder="Musterstraße 1, 12345 Musterstadt", height=100)
    u_snr = st.text_input("Steuernummer / Identifikationsnummer", help="Steht oben links auf dem Steuerbescheid.")

with tab2:
    st.subheader("Angaben zum Bescheid")
    u_fa = st.text_input("Name des Finanzamts", placeholder="z.B. Finanzamt Berlin-Mitte")
    u_datum = st.date_input("Datum Ihres Bescheids")

with tab3:
    st.subheader("Warum legen Sie Einspruch ein?")
    fall = st.selectbox("Wählen Sie den Grund:", [
        "Grundsteuer: Wertfeststellung (Bodenrichtwert)",
        "Kapitalerträge: Verlustverrechnung § 20 Abs. 6",
        "Kryptowährungen: Haltefrist § 23",
        "Allgemeine Fristwahrung (Begründung folgt)"
    ])


# --- 6. TEXTLOGIK & GENERIERUNG ---
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

st.divider()

if st.button("Jetzt Einspruch-PDF generieren", type="primary", use_container_width=True):
    if u_name and u_snr and u_fa and u_adresse:
        try:
            pdf_bytes = create_pdf(u_name, u_adresse, u_snr, u_fa, u_datum, text, betreff)
            st.success("✅ Dein Einspruch wurde erfolgreich erstellt! Klicke unten zum Download.")
            st.download_button(
                label="📥 PDF jetzt herunterladen & speichern",
                data=pdf_bytes,
                file_name=f"Einspruch_{u_name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
    else:
        st.error("⚠️ Bitte fülle alle Textfelder in den Reitern aus (Name, Anschrift, Steuernummer, Finanzamt).")


# --- 7. RATGEBER & MISSION ---
st.divider()
st.subheader("Hintergrund & Mission")
st.markdown("""
> *"Ich arbeite beim Finanzamt und ärgere mich täglich darüber, wie viele Menschen Geld auf der Straße liegen lassen, 
> weil sie ihre falschen Steuerbescheide einfach akzeptieren. Viele Menschen haben immer noch Angst davor, 
> sich gegen die Finanzbehörde zu stellen. Doch so ein Steuerbescheid ist kein unumstößliches Gesetz, sondern "nur" ein Verwaltungsakt, der fehleranfällig ist. Dieses Tool soll den Menschen dabei helfen, 
> sich das Geld zurückzuholen, das ihnen rechtmäßig zusteht. Sie sollen nicht unnötig zu viel bezahlen, nur weil der Prozess zu kompliziert wirkt."*
""")

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
    Ihr Einspruch muss in der Regel spätestens **einen Monat** nach Bekanntgabe des Bescheids beim Finanzamt eingehen. **Wichtig**: Prüfen Sie den Poststempel oder das Datum ihres Bescheides. Rechnen Sie auf dieses Datum **3 Tage** dazu (Bekanntgabefiktion § 122 AO). Bis zu diesem Tag wahren Sie mit ihrem Einspruch die gesetzliche Frist. Danach wird der Bescheid 
    rechtskräftig und ihr Einspruch wird vom Finanzamt nicht mehr berücksichtigt.
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
    ('Verböserung'), muss das Amt Sie vorher warnen. Sie können ihren Einspruch dann immer noch zurücknehmen. Es wird nichts geändert und es bleibt bei dem ursprünglichen Steuerbescheid. Sie haben also nichts zu verlieren, es kann sich nur für Sie lohnen!
    """)
