/**
 * Betrachtungshorizont: Eine Woche
 * Berechne POC der Vorwoche
 * Betrachte Schlusskurs der Vorwoche (Freitag)
 * Short:
 *  - Liegt der Schlusskurs der Vorwoche (Freitag) unter dem POC?
 *  - Steigt der Kurs in der aktuellen Woche (ab Montag) in Richtung POC?
 *  - Strategie:
 *      - Annahme: Kurs bewegt sich aufwärts in Richtung POC und prallt nach unten ab
 *      - ENTRY: POC
 *      - Stop-Loss 1 (SL 1): POC + X€
 *      - Stop-Loss 2 (SL 2): HIGH der Vorwoche (außer HIGH == POC)
 *      - Take Profit 1 (TP1): "Schlusskurs der Vorwoche (Freitag) + X€"
 *      - Take Profit 2 (TP2): "Schlusskurs der Vorwoche (Freitag)"
 *      - Take Profit 3 (TP3): "Schlusskurs der Vorwoche (Freitag) - X€"
 *      - TODO: Wie legen wir X fest? Soll X überall gleich sein?
 *      - TIMEOUT: Schlusskurs der aktuellen Woche am Freitag 23:00 Uhr, wenn in der Woche weder
 *          - SL1 - SL2
 *          - TP1 - TP3
 *        getriggerd wurde
 * Long:
 *  - Liegt der Schlusskurs der Vorwoche (Freitag) über dem POC?
 *  - Fällt der Kurs in der aktuellen Woche (ab Montag) in Richtung POC?
 *  - Strategie:
 *      - Annahme: Der Kurs bewegt sich abwärts in Richtung POC und prallt nach oben ab
 *      - ENTRY: POC
 *      - Stop-Loss 1 (SL 1): POC - X€
 *      - Stop-Loss 2 (SL 2): LOW der Vorwoche (außer LOW == POC)
 *      - Take Profit 1 (TP1): "Schlusskurs der Vorwoche (Freitag) - X€"
 *      - Take Profit 2 (TP2): "Schlusskurs der Vorwoche (Freitag)"
 *      - Take Profit 3 (TP3): "Schlusskurs der Vorwoche (Freitag) + X€"
 *      - TODO: Wie legen wir X fest? Soll X überall gleich sein?
 *      - TIMEOUT: Schlusskurs der aktuellen Woche am Freitag 23:00 Uhr, wenn in der Woche weder
 *          - SL1 - SL2
 *          - TP1 - TP3
 *        getriggerd wurde
 * 
 * Verfeinerungen:
 *  - ATR für TP-Strategien
 *  - ENTRY muss bis Zeitpunkt T (bspw. Mittwochs 18:00) erreicht werden. Sonst findet kein Trade statt.
 *  - X€ durch Anzahl Ticks ersetzen
 */

pub fn compute() {
    println!("poc resistance");
}