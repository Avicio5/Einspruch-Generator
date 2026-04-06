import streamlit as st
from datetime import date

# 1. Layout & Titel
st.set_page_config(page_title="Tax-Insider Einspruch-Generator", page_icon="⚖️")
st.title("⚖️ Einspruch-Generator für Anleger")
st.subheader("Erstelle in 2 Minuten ein rechtssicheres Schreiben an dein Finanzamt.")

# 2. Eingabemaske (Sidebar für Nutzerdaten)
with st.sidebar:
    st.header("Deine Daten")
    name = st.text_input("Vollständiger Name")
    adresse = st.text_area("Anschrift")
    steuernummer = st.text_input("Steuernummer / ID-Nr.")
    finanzamt = st.text_input("Zuständiges Finanzamt")

# 3. Den Fall auswählen (Deine Fach-Expertise)
st.write("---")
st.header("Was ist der Grund für den Einspruch?")
fall_typ = st.selectbox(
    "Wähle das Thema deines Falls:",
    ["Verlustverrechnungsbeschränkung (§ 20 Abs. 6 EStG)", 
     "Krypto-Gewinne / Haltefrist", 
     "Werbungskosten bei Kapitaleinkünften",
     "Sonstiger Grund"]
)

datum_bescheid = st.date_input("Datum des Steuerbescheids", date.today())
aktenzeichen = st.text_input("Bescheid-Datum / Kennzeichen (optional)")

# 4. Die Insider-Logik (Textbausteine)
def generiere_text(fall):
    if "Verlustverrechnung" in fall:
        return f"""hiermit lege ich Einspruch gegen den Einkommensteuerbescheid vom {datum_bescheid} ein.
        
Begründung: Die aktuelle Verlustverrechnungsbeschränkung für Termingeschäfte gemäß § 20 Abs. 6 Satz 5 EStG ist nach Ansicht vieler Experten verfassungswidrig. Ich beantrage daher das Ruhen des Verfahrens im Hinblick auf das laufende Revisionsverfahren beim BFH (Az. VIII R 11/22)."""
    
    elif "Krypto" in fall:
        return f"""hiermit lege ich Einspruch gegen den Einkommensteuerbescheid vom {datum_bescheid} ein.
        
Begründung: Die Besteuerung der veräußerten Krypto-Assets wurde fehlerhaft vorgenommen. Insbesondere wurde die einjährige Haltefrist gemäß § 23 EStG nicht korrekt berücksichtigt..."""
    
    else:
        return "Bitte formuliere hier kurz deinen individuellen Grund..."

# 5. Output-Bereich
if st.button("Einspruch-Text generieren"):
    if not name or not steuernummer:
        st.error("Bitte gib mindestens deinen Namen und deine Steuernummer an.")
    else:
        finaler_text = f"""
{name}
{adresse}

An das 
Finanzamt {finanzamt}

Datum: {date.today()}

Steuernummer: {steuernummer}

**Einspruch gegen den Einkommensteuerbescheid vom {datum_bescheid}**

Sehr geehrte Damen und Herren,

{generiere_text(fall_typ)}

Ich bitte um Bestätigung des Eingangs.

Mit freundlichen Grüßen,
{name}
        """
        st.success("Dein Schreiben ist fertig!")
        st.text_area("Kopiere diesen Text:", finaler_text, height=400)
        st.info("Tipp: In der Vollversion kannst du dies direkt als PDF herunterladen.")