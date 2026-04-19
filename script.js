// Tab-Logik
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; }
    tablinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// PDF-Generator
document.getElementById('generateBtn').addEventListener('click', function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Daten auslesen
    const name = document.getElementById('u_name').value;
    const adresse = document.getElementById('u_adresse').value;
    const snr = document.getElementById('u_snr').value;
    const fa = document.getElementById('u_fa').value;
    const datumRaw = document.getElementById('u_datum').value;
    const fall = document.getElementById('u_fall').value;

    if (!name || !snr || !fa) {
        alert("Bitte fülle mindestens Name, Steuernummer und Finanzamt aus!");
        return;
    }

    const datum = datumRaw ? new Date(datumRaw).toLocaleDateString('de-DE') : "[Datum]";
    const heute = new Date().toLocaleDateString('de-DE');

    // Textlogik aus deinem Python-Code
    let betreff = "";
    let text = "";

    if (fall === "grundsteuer") {
        betreff = "Einspruch gegen den Bescheid über den Grundsteuerwert";
        text = "hiermit lege ich Einspruch gegen den Feststellungsbescheid über den Grundsteuerwert ein. Es bestehen ernsthafte Zweifel an der rechtmäßigen Ermittlung der zugrunde gelegten Bodenrichtwerte (§ 247 BewG). Um eine Fehlbewertung meines Grundstücks auszuschließen, wird um eine detaillierte Überprüfung der Wertfeststellung gebeten. Zudem verweise ich auf die aktuell laufenden verfassungsrechtlichen Prüfungen.";
    } else if (fall === "kapital") {
        betreff = "Einspruch gegen den Einkommensteuerbescheid (Kapitalerträge)";
        text = "hiermit lege ich Einspruch gegen den oben genannten Bescheid ein. Die steuerliche Behandlung der Kapitalerträge, insbesondere die Beschränkung der Verlustverrechnung bei Termingeschäften, wird im Hinblick auf die laufenden Verfahren vor dem Bundesfinanzhof (BFH VIII R 11/22) beanstandet. Ich beantrage hiermit das Ruhen des Verfahrens bis zu einer endgültigen Entscheidung.";
    } else if (fall === "krypto") {
        betreff = "Einspruch gegen den Einkommensteuerbescheid (Kryptowerte)";
        text = "hiermit lege ich Einspruch gegen den Bescheid ein. Die Veräußerungsgeschäfte mit Kryptowerten wurden fälschlicherweise als steuerpflichtig behandelt. Gemäß § 23 EStG sind private Veräußerungsgeschäfte steuerfrei, wenn die Haltefrist von einem Jahr überschritten wurde. Ich bitte um erneute Prüfung der eingereichten Daten.";
    } else {
        betreff = "Fristwahrender Einspruch gegen den Steuerbescheid";
        text = "hiermit lege ich fristwahrend Einspruch gegen den oben genannten Bescheid ein. Zur Vermeidung des Eintritts der Bestandskraft wird dieser Einspruch hiermit form- und fristgerecht erhoben. Eine ausführliche Begründung werde ich Ihnen nach Sichtung meiner Unterlagen in einem gesonderten Schreiben nachreichen.";
    }

    // PDF Aufbau
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text("Privates Einspruchsschreiben - Fachportal für Steuerrecht", 190, 10, { align: "right" });

    doc.setFontSize(11);
    doc.text(name, 20, 30);
    doc.text(doc.splitTextToSize(adresse, 80), 20, 35);

    doc.text("An das", 20, 55);
    doc.text("Finanzamt " + fa, 20, 60);

    doc.text("Datum: " + heute, 190, 80, { align: "right" });

    doc.setFont("helvetica", "bold");
    doc.text(betreff + " vom " + datum, 20, 95);
    doc.text("Steuernummer: " + snr, 20, 102);

    doc.setFont("helvetica", "normal");
    const bodyText = "Sehr geehrte Damen und Herren,\n\n" + text + "\n\nMit freundlichen Grüßen,\n\n" + name;
    const splitText = doc.splitTextToSize(bodyText, 170);
    doc.text(splitText, 20, 115);

    doc.save(`Einspruch_${name.replace(/\s+/g, '_')}.pdf`);
});
