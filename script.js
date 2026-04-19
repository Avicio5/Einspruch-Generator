document.getElementById('generateBtn').addEventListener('click', function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const name = document.getElementById('userName').value || "Gast";
    const object = document.getElementById('objectName').value || "Unbekanntes Objekt";

    // PDF Inhalt gestalten
    doc.setFont("helvetica", "bold");
    doc.setFontSize(22);
    doc.text("GaragenKapital - Report", 20, 30);
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(14);
    doc.text(`Erstellt für: ${name}`, 20, 50);
    doc.text(`Objekt: ${object}`, 20, 60);
    
    doc.text("Dies ist ein automatisch generiertes Dokument.", 20, 80);

    // PDF Download
    doc.save(`Analyse_${object}.pdf`);
});
