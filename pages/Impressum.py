import streamlit as st

# Seite konfigurieren
st.set_page_config(page_title="Impressum | Steuer-Einspruchgenerator", layout="wide")

# Der komplette CSS- und HTML-Block von deiner anderen Seite
# Ich habe die Navigationsleiste entfernt, damit das Streamlit-Menü sauber bleibt.
impressum_html = """
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root {
      --bg: #f9f8f6;
      --surface: #ffffff;
      --border: #e2ddd6;
      --navy: #0f2444;
      --text: #1a1814;
      --text-muted: #5c564e;
      --text-dim: #9b9590;
    }

    .main-container {
        max-width: 780px;
        margin: 0 auto;
        padding: 40px 20px;
        background: var(--bg);
        font-family: "Plus Jakarta Sans", sans-serif;
        color: var(--text);
    }

    .page-tag {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--navy);
        margin-bottom: 14px;
    }

    h1 {
        font-family: "Fraunces", serif;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-bottom: 8px;
        color: var(--text);
    }

    .subtitle {
        font-size: 14px;
        color: var(--text-dim);
        margin-bottom: 48px;
        padding-bottom: 32px;
        border-bottom: 1px solid var(--border);
    }

    h2 {
        font-family: "Fraunces", serif;
        font-size: 20px;
        font-weight: 800;
        margin: 40px 0 14px;
        color: var(--text);
    }

    h3 {
        font-size: 15px;
        font-weight: 700;
        margin: 24px 0 10px;
        color: var(--text);
    }

    p {
        font-size: 15px;
        color: var(--text-muted);
        line-height: 1.8;
        font-weight: 300;
        margin-bottom: 16px;
    }

    .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 40px 0;
    }
    
    /* Streamlit Elemente verstecken für den cleanen Look */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>

<div class="main-container">
    <div class="page-tag">Rechtliches</div>
    <h1>Impressum</h1>
    <p class="subtitle">Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)</p>

    <h2>Verantwortlicher Betreiber</h2>
    <p>
        Fynn Korbas<br>
        Sibyllenweg 16<br>
        46537 Dinslaken<br>
        Deutschland
    </p>

    <h2>Kontakt</h2>
    <p>
        E-Mail: <a href="mailto:info@garagenkapital.de" style="color: var(--navy);">info@garagenkapital.de</a>
    </p>

    <h2>Umsatzsteuer</h2>
    <p>Eine Umsatzsteuer-Identifikationsnummer liegt nicht vor. Die Website wird privat betrieben.</p>

    <h2>Inhaltlich verantwortlich gemäß § 18 Abs. 2 MStV</h2>
    <p>
        Fynn Korbas<br>
        Sibyllenweg 16, 46537 Dinslaken
    </p>

    <hr class="section-divider">

    <h2>Haftungsausschluss</h2>

    <h3>Haftung für Inhalte</h3>
    <p>Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann jedoch keine Gewähr übernommen werden. Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Die Inhalte dieser Website dienen ausschließlich zu Informationszwecken und stellen keine Anlage-, Rechts- oder Steuerberatung dar.</p>

    <h3>Keine Anlageberatung</h3>
    <p>Alle auf dieser Website veröffentlichten Informationen, Renditeberechnungen, Marktanalysen und Einschätzungen sind unverbindlich und dienen nur zur allgemeinen Information. Sie stellen ausdrücklich keine Empfehlung zum Kauf oder Verkauf von Immobilien oder anderen Anlagen dar. Investitionsentscheidungen sollten immer auf Basis eigener Recherchen und im Zweifel mit professioneller Beratung getroffen werden.</p>

    <h3>Haftung für Links</h3>
    <p>Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte kein Einfluss besteht. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Zum Zeitpunkt der Verlinkung wurden die verlinkten Seiten auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar.</p>

    <h3>Urheberrecht</h3>
    <p>Die durch den Seitenbetreiber erstellten Inhalte und Werke auf dieser Website unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.</p>
</div>
"""

st.markdown(impressum_html, unsafe_allow_html=True)
