/**
 * Berechne POC der Vorwoche
 * Betrachte Schlusskurs der Vorwoche (Freitag)
 * Long:
 *  - Liegt der Schlusskurs der Vorwoche (Freitag) unter dem POC?
 *  - Steigt der Kurs in der aktuellen Woche (ab Montag) über den Schlusskurs der Vorwoche?
 *  - Strategie:
 *      - Der Kurs bewegt sich aufwärts in Richtung POC
 *      - Stop-Loss: Schlusskurs der Vorwoche (Freitag) - X€
 *      - Take Profit 1 (TP1): "POC - X€"
 *      - Take Profit 2 (TP2): "POC + X€"
 *      - TODO: Wie legen wir X fest? Soll X überall gleich sein?
 *      - EXIT: Schlusskurs der aktuellen Woche am Freitag 23:59 Uhr, wenn in der Woche weder
 *          - Stop-Loss
 *          - TP1
 *          - TP2
 *        getriggerd wurde
 * Short:
 *  - Liegt der Schlusskurs der Vorwoche (Freitag) über dem POC?
 *  - Fällt der Kurs in der aktuellen Woche (ab Montag) unter den Schlusskurs der Vorwoche?
 *  - Strategie:
 *      - Der Kurs bewegt sich abwärts in Richtung POC
 *      - Stop-Loss: Schlusskurs der Vorwoche (Freitag) + X€
 *      - Take Profit 1 (TP1): "POC + X€"
 *      - Take Profit 2 (TP2): "POC - X€"
 *      - TODO: Wie legen wir X fest? Soll X überall gleich sein?
 *      - EXIT: Schlusskurs der aktuellen Woche am Freitag 23:59 Uhr, wenn in der Woche weder
 *          - Stop-Loss
 *          - TP1
 *          - TP2
 *        getriggerd wurde
 */

pub fn compute() {
    println!("weekly poc");
}