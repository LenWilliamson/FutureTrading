pub use crate::data_models::*;
use chrono::format::ParseResult;
use chrono::prelude::*;
use ordered_float::OrderedFloat;
/**
 * Betrachtungshorizont: Eine Woche (Mo ab 01:00 - Fr bis 23:00)
 * Berechne POC der Vorwoche
 * Betrachte Schlusskurs der Vorwoche (Freitag)
 * Short:
 *  - Liegt der Schlusskurs der Vorwoche (Freitag) unter dem POC?
 *  - Steigt der Kurs in der aktuellen Woche (ab Montag) in Richtung POC?
 *  - Wir betrachten immer "echt kleiner" < und "echt größer" >
 *  - Strategie:
 *      - Annahme: Kurs bewegt sich aufwärts in Richtung POC und prallt nach unten ab
 *      - ENTRY: POC
 *      - Stop-Loss 1 (SL 1): POC + X€
 *      - Stop-Loss 2 (SL 2): HIGH der Vorwoche
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
 *      - Stop-Loss 2 (SL 2): LOW der Vorwoche
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
 *
 * Danach:
 *  -> https://www.pola.rs/ (Python migrieren)
 *  -> https://docs.rs/plotters/0.3.2/plotters/ (Plotly ersetzen)
 *  -> Alternativ: Plotly.rs -> https://github.com/igiagkiozis/plotly
 *
 * +++      +++      +++
 *
 * Testfall 1:
 *  - Zeitraum 2022-03:
 *      - Schlusskurs Freitag (2022-03-04 23:00): 39_004.73USDT
 *      - Wähle POC: 42_100.00USDT (POC so wählen das Trade nicht getriggert wird)
 *      - Short Trade findet statt (2022-03-09 09:00)
 *      - Höchster Kurs in der Woche vom Short Trade (ab Zeitpunkt des ENTRY): (2022-03-09 16:00): 42_594.06USDT => TESTEN
 *      - Niedrigster Kurs in der Woche vom Short Trade (ab Zeiptunkt des ENTRY): (2022-03-11 03:00): 38_223.60USDT => TESTEN
 *      - Schlusskurs Freitag (2022-03-11 23:00): 38_916.69USDT
 *      - Prüfe anhand der Daten der Vorwoche ob korrekterweise ein Shorttrade vorliegt
 *  - Prüfe:
 *      - Wird der Entry beim POC ausgelöst
 *      - SL1:
 *          - Wähle X = 494.07USDT => Trade läuft weiter
 *          - Wähle X = 500.00USDT => Trade läuft weiter
 *          - Wähle X = 494.06USDT => Ausgestopped, da die Bedingung "<" nicht erfüllt
 *          - Wähle X = 400.00USDT => Ausgestopped
 *      - SL2:
 *          - Berechne High & Low der Vorwoche => Testen, da Daten erst ab Dienstag vorliegen
 *              - HIGH (2022-03-02 16:00): 44_819.39USDT => Wähle HIGH da Shorttrade
 *              - LOW ist nicht am 2022-02-28 um 00-00-00 bei 37_330.23USDT da Außerhalb Zeitinterval => Testen
 *              - LOW ist 37_450.17USDT  2022-02-28 um 01-00-00
 *          - Trade läuft weiter
 *          - Setze High der Vorwoche künstlich auf 42_200.00USDT => Ausgestopped
 *      - TP1:
 *          - Wähle X = 1_000.00USDT => Gewinn = 42_100.00 - (39_004.73USDT + 1_000.00USDT)
 *          - ......nonsense: Wähle X = 4_000.00USDT => TIMEOUT mit Gewinn (macht kein Sinn, da oberhalb von POC)
 *      - TP2: Wähle X = 0.00USDT => Gewinn
 *      - TP3:
 *          - Wähle X = 500.00USDT => Gewinn = 42_100.00 - (39_004.73USDT - 500.00USDT)
 *          - Wähle X = 1_000.00USDT => TIMEOUT mit Gewinn
 *      - TIMEOUT mit Verlust fehlt => künstlich erzeugen
 *
 * Testfall 2:
 *  - Zeitraum 2022-02:
 *      - Schlusskurs Freitag (2022-02-25 23:00): 39_424.14USDT
 *      - Wähle POC: 38_100.00USDT (POC so wählen das Trade nicht getriggert wird)
 *      - Long Trade findet nicht am (2022-02-27 20:00) statt (da Wochenende) => Testen ob der Filter funktioniert, dass wir nur (Mo ab 01:00 - Fr bis 23:00) prüfen
 *      - Long Trade findet statt am (2022-02-28 01:00)
 *      - Höchster Kurs in der Woche vom Short Trade (ab Zeitpunkt des ENTRY):(2022-03-02 16:00): 45_400.39USDT => TESTEN
 *      - Niedrigster Kurs in der Woche vom Short Trade (ab Zeiptunkt des ENTRY, hier sogar gleich dem Zeitpunkt des ENTRY): (2022-02-28 01:00): 37_450.17USDT => TESTEN
 *      - Schlusskurs Freitag (2022-03-04 23:00): 39_004.73USDT
 *      - Prüfe anhand der Daten der Vorwoche ob korrekterweise ein Longtrade vorliegt
 *  - Prüfe:
 *      - Wird der Entry beim POC ausgelöst
 *      - SL1:
 *          - Wähle X = 1_000.00USDT => Trade läuft weiter
 *          - Wähle X = 649.84USDT => Trade läuft weiter
 *          - Wähle X = 649.83USDT => Ausgestopped, da die Bedingung ">" nicht erfüllt
 *          - Wähle X = 400.00USDT => Ausgestopped
 *      - SL2:
 *          - Berechne High & Low der Vorwoche => Wähle LOW da Long Trade
 *              - HIGH (2022-02-24 21:00): 39_843.00USDT
 *              - LOW ist 34_322.28USDT  2022-02-24 um 06-00-00
 *          - Trade läuft weiter
 *          - Setze Low der Vorwoche künstlich auf 37_800.00USDT => Ausgestopped
 *      - TP1:
 *          - Wähle X = 400.00USDT => GEWINN = (39_424.14 - 400) - 38_100.00
 *          - Keine weiteren Fälle hier, da TP1 die risikoaverse Version ist
 *      - TP2: Wähle X = 0.00USDT => Gewinn
 *      - TP3:
 *          - Wähle X = 5_000.00USDT => GEWINN = (39_424.14 + 5_000.00) - 38_000.00
 *          - Wähle X = 10_000.00USDT => TIMEOUT mit Gewinn
 *      - TIMEOUT mit Verlust fehlt => künstlich erzeugen
 *
 * Weiterer Testfall:
 *  - Short Trade registriert, aber kein Eintritt
 *  - Long Trade registriert, aber kein Eintritt
 *  - Jede Woche liefert resulstat mit Metadaten
 *
 * Aktuell nimmst du nur den ersten entry, was ist wenn es zwei entries gibt? Wir wirkt das auf die Margin?
 *
 * Wenn die Daten in 1Monatstabellen vorliegen muss korrekt der nächste Monat geladen werden
 *
 * Test ob höchster und niedrigster Kurs ab Zeiptunkt des ENTRY richtig bestimmt wird
 *
 * Wir brauchen einen Fall in dem der Trade nicht closed und TIMEOUT mit Gewinn / Verlust hat
 *
 * Wir müssen testen ob anhand der Daten der Vorwoche korrekt bestimmt wird ob wir einen Long oder
 * Short Trade erwarten
 *  
 * Unabhängig von Short oder Long soll es eine Funktion geben: Trade Triggerd der als Argument übergeben wird
 * ob es ein Long oder Short Trade ist. Diese prüft ob der Trade valide ist für die Kerze in der der Trade getriggerd wird.
 *  - Wir müssen Shorttrade prüfen, wenn der Eröffnungskurs unter dem POC ist
 *  - Was passiert wenn in der ersten Kerze der Trade ausgelöst wird, da POC in [Low, High], aber Low bzw. High schon ausstoppen
 */
use serde::Deserialize;
use std::path::Path;
use std::marker::Copy;

#[derive(Debug, Deserialize)]
enum TimeStandardKind {
    Utc,
    Local,
}

#[derive(Debug)]
enum TradeKind {
    Long,
    Short,
    None,
}

#[derive(Debug)]
struct TimeInterval {
    start_day: chrono::Weekday,
    start_h: u32,
    end_day: chrono::Weekday,
    end_h: u32,
}

#[derive(Debug)]
/**
 * TODO
 * Ergänze SL und TP und evaluiere dann
 * Speichere Daten als JSON und visualisiere sie dann
 */
struct PocResistance {
    time_standard: TimeStandardKind,
    time_interval: TimeInterval,
    data_path: String,
    data_depth: Vec<String>,
}

#[derive(Debug)]
struct TradeInfo {
    // Bezieht sich auf die Vorwoche
    last_trade_price: f32,
    lowest_price: f32,
    highest_price: f32,
    trade: TradeKind,
}

#[derive(Debug)]
struct TradeStat {
    // Bezieht sich auf die Woche vom Trade
    entry: i64,
    poc: f32, // Kurs zu dem wir kaufen
    last_trade_price: f32,
    lowest_price_since_entry: f32,
    highest_price_since_entry: f32,
    date_lowest_price: i64,
    date_highest_price: i64,
    records: Vec<ohlc::OhlcCsvRecord>,
}

#[derive(/* Copy, */ Debug)]
struct TradeEvaluation {
    trade_info: TradeInfo,
    trade_stat: std::option::Option<TradeStat>, // None if no trade happend
}

// impl Copy for TradeEvaluation {}

impl TradeEvaluation {
    fn compute_profit_and_losses(&self, strategy: &Strategy) -> ProfitAndLosses {
        /*
         * Check if trade_stat is not none
         * If none -> done with empty i.e. 0 values everywhere
         * else compute
         *
         * Eigentlich kann man auch ein Vec<Strategy> übergeben?
         */

        // Stop Loss
        let mut condition = strategy.stop_loss_condition;
        let mut entry_time_stamp = self.compute_entry_time_stamp(condition);
        // unwrap konsumiert => deswegen .as_ref() hinzufügen let x = self.trade_stat.as_ref().unwrap().poc;
        let mut poc = match &self.trade_stat {
            Some(x) => x.poc,
            None => panic!("No POC found"),
        };
        let mut profit = match entry_time_stamp {
            Some(ts) => Some(self.compute_profit(
                ts,
                &self.trade_info.trade,
                poc,
            )),
            None => None,
        };

        let stop_loss = StopLoss {
            condition,
            entry_time_stamp,
            profit,
        };

        let mut take_profit_events = Vec::<TakeProfit>::new();
        // let mut timeout_events = Vec::<Option<Timeout>>::new();
        // Funktional lösen
        for tp in &strategy.take_profit_conditions {
            condition = *tp;
            entry_time_stamp = self.compute_entry_time_stamp(condition);
            poc = match &self.trade_stat {
                Some(x) => x.poc,
                None => panic!("No POC found"),
            };
            profit = match entry_time_stamp {
                Some(ts) => Some(self.compute_profit(
                    ts,
                    &self.trade_info.trade,
                    poc
                )),
                None => None,
            };
            let triggered = match entry_time_stamp {
                Some(ts) => true,
                None => false,
            };
            let last_trade_price = match &self.trade_stat {
                Some(x) => x.last_trade_price,
                None => panic!("No last trade price"),
            };
            let timeout = match triggered {
                false => Some(Timeout {
                    condition: last_trade_price,
                    profit: match self.trade_info.trade {
                        TradeKind::Short => {
                            poc - last_trade_price
                        }
                        TradeKind::Long => {
                            last_trade_price - poc
                        },
                        TradeKind::None => panic!("Cannot compute profit for TradeKind::None")
                    }
                }),
                true => None,
            };
            let take_profit = TakeProfit {
                condition,
                triggered,
                entry_time_stamp,
                profit,
                timeout,
            };
            take_profit_events.push(take_profit);
            // timeout_events.push(timeout);
        }

        

        ProfitAndLosses {
            stop_loss,
            take_profit: take_profit_events,
            // timeout: timeout_events,
        }
    }

    // Aufruf mit &self und daann self.trade_stat.records geht nicht
    // Moving out of reference Error
    fn compute_entry_time_stamp(&self, condition: f32) -> Option<i64> {
        // Lediglich der erste Trade wird genommen
        let records = match &self.trade_stat {
            Some(x) => &x.records,
            None => panic!("No OHLC record found"),
        };
        match records
            .iter()
            .find(|&x| x.low <= condition && condition <= x.high)
        {
            Some(v) => Some(v.ots),
            None => None,
        }
    }

    fn compute_profit(
        &self,
        entry_ts: i64,
        trade_kind: &TradeKind,
        entry_price: f32
    ) -> f32 {
        let records = match &self.trade_stat {
            Some(x) => &x.records,
            None => panic!("No OHLC record found"),
        };
        match trade_kind {
            TradeKind::Short => {
                let high = records.iter().find(|&x| x.ots == entry_ts).unwrap().high;
                // max loss entry - high (should be negative) and min profit
                entry_price - high
            }
            TradeKind::Long => {
                let low = records.iter().find(|&x| x.ots == entry_ts).unwrap().low;
                // max loss entry - high (should be negative) and min profit
                low - entry_price
            },
            TradeKind::None => panic!("Cannot compute profit for TradeKind::None")
        }
    }
}

#[derive(Debug)]
struct TakeProfit {
    condition: f32,
    triggered: bool, // if true timeout == None
    entry_time_stamp: Option<i64>,
    profit: Option<f32>,
    timeout: Option<Timeout>,
}

#[derive(Debug)]
struct Strategy {
    stop_loss_condition: f32,
    take_profit_conditions: Vec<f32>,
}

#[derive(Debug)]
struct StopLoss {
    condition: f32,
    entry_time_stamp: Option<i64>,
    profit: Option<f32>, // profit < 0 is a loss
}

#[derive(Debug)]
struct Timeout {
    condition: f32, // used to be timestamp -> Now last traded price
    profit: f32,
}



#[derive(Debug)]
struct ProfitAndLosses {
    stop_loss: StopLoss,
    take_profit: Vec<TakeProfit>,
    // timeout: Vec<Option<Timeout>>,
}

impl PocResistance {
    fn eval_trade(&self, cw: u32) -> TradeEvaluation {
        // compute POC for calendar week cw - 1 (for 1 < cw < 52)
        let vp = self.compute_volume_profile(cw);
        dbg!(&vp);
        let ohlc_prev = self.load_ohlc(cw - 1);
        let ohlc_curr = self.load_ohlc(cw);
        // dbg!(ohlc_prev.records.first().unwrap());
        // dbg!(ohlc_prev.records.last().unwrap());

        let last_trade_price = ohlc_prev.records.last().unwrap().close;
        let trade = PocResistance::determine_trade_kind(last_trade_price, vp.poc);

        let trade_info = TradeInfo {
            last_trade_price,
            lowest_price: ohlc_prev
                .records
                .iter()
                .min_by_key(|&x| OrderedFloat(x.low))
                .unwrap()
                .low,
            highest_price: ohlc_prev
                .records
                .iter()
                .max_by_key(|&x| OrderedFloat(x.high))
                .unwrap()
                .high,
            trade,
        };

        let trade_stat = match PocResistance::determine_entry(&ohlc_curr, vp.poc) {
            Some(e) => {
                let l = ohlc_curr
                    .records
                    .iter()
                    .filter(|&x| x.ots >= e)
                    .min_by_key(|&x| OrderedFloat(x.low))
                    .unwrap();
                let h = ohlc_curr
                    .records
                    .iter()
                    .filter(|&x| x.ots >= e)
                    .max_by_key(|&x| OrderedFloat(x.high))
                    .unwrap();
                Some(TradeStat {
                    entry: e,
                    poc: vp.poc,
                    last_trade_price: ohlc_curr.records.last().unwrap().close,
                    lowest_price_since_entry: l.low,
                    highest_price_since_entry: h.high,
                    date_lowest_price: l.ots,
                    date_highest_price: h.ots,
                    records: ohlc_curr.records,
                })
            }
            None => None,
        };

        dbg!(&trade_stat.as_ref().unwrap().entry);
        dbg!(&trade_stat.as_ref().unwrap().poc);
        dbg!(&trade_stat.as_ref().unwrap().last_trade_price);
        dbg!(&trade_stat.as_ref().unwrap().lowest_price_since_entry);
        dbg!(&trade_stat.as_ref().unwrap().highest_price_since_entry);
        dbg!(&trade_stat.as_ref().unwrap().date_lowest_price);
        dbg!(&trade_stat.as_ref().unwrap().date_highest_price);
        TradeEvaluation {
            trade_info,
            trade_stat,
        }
    }

    fn compute_volume_profile(&self, cw: u32) -> volume_profile::VolumeProfile {
        let t = (cw - 1).to_string(); // time e.g. number of calender week
        let e = ".csv"; // (file) extension
        let f = "KW".to_string() + &t + &e; // (complete) file
        let p = Path::new(&self.data_path)
            .join(&self.data_depth[0])
            .join("volumeProfile")
            .join(f);
        volume_profile::VolumeProfile::read_from_path(p.to_str().unwrap()).unwrap()
    }

    fn load_ohlc(&self, cw: u32) -> ohlc::OhlcData {
        let t = cw.to_string(); // time e.g. number of calender week
        let e = ".csv"; // (file) extension
        let f = "KW".to_string() + &t + &e; // (complete) file
        let p = Path::new(&self.data_path)
            .join(&self.data_depth[0])
            .join("ohlc")
            .join(f);
        let mut ohlc = ohlc::OhlcData::read_from_path(p.to_str().unwrap()).unwrap();

        // Filter ohlc records to correct interval
        // ohlc.records.iter().filter()
        let predicate = |x: &ohlc::OhlcCsvRecord| -> bool {
            let ots = NaiveDateTime::from_timestamp(x.ots / 1000, 0);
            let weekend =
                ots.weekday() == chrono::Weekday::Sat || ots.weekday() == chrono::Weekday::Sun;
            let too_early = ots.hour() < self.time_interval.start_h
                && ots.weekday().number_from_monday()
                    <= self.time_interval.start_day.number_from_monday();
            let too_late = ots.hour() >= self.time_interval.end_h
                && ots.weekday().number_from_monday()
                    >= self.time_interval.end_day.number_from_monday() - 1;
            // dbg!(ots);
            // dbg!(weekend);
            // dbg!(too_early);
            // dbg!(too_late);
            !(weekend || too_early || too_late)
        };
        ohlc.records.retain(predicate);
        ohlc
    }

    fn determine_trade_kind(last_trade_price: f32, poc: f32) -> TradeKind {
        let b = last_trade_price < poc;
        if last_trade_price < poc {
            TradeKind::Short
        } else if last_trade_price > poc {
            TradeKind::Long
        } else {
            TradeKind::None
        }
    }

    fn determine_entry(ohlc: &ohlc::OhlcData, poc: f32) -> std::option::Option<i64> {
        // Lediglich der erste Trade wird genommen
        match ohlc.records.iter().find(|&x| x.low <= poc && poc <= x.high) {
            Some(v) => Some(v.ots),
            None => None,
        }
    }
}

/* fn get_unix_ts(date: &str) -> ParseResult<i64> {
    let ts = Utc
        .datetime_from_str(&date, "%Y-%m-%d_%H:%M:%S")?
        .timestamp_millis();
    Ok(ts)
}
 */

pub fn compute(/* Strategy */) {
    let poc_resistance = PocResistance {
        time_standard: TimeStandardKind::Utc,
        time_interval: TimeInterval {
            start_day: chrono::Weekday::Mon,
            start_h: 1,
            end_day: chrono::Weekday::Sat,
            end_h: 23, // wir vergleichen immer auf ein offenes Intervall <
        },
        data_path: "/media/len/ExterneFestplateLenCewa/DataBase/data/".to_string(),
        data_depth: vec!["2022".to_string()],
    };

    

    let x = poc_resistance.eval_trade(10);
    // let poc = 42_100.0; // auf den musst du vorher zugreifen
    let poc =  x.trade_stat.as_ref().unwrap().poc;
    let lst = x.trade_info.last_trade_price;
    let s = Strategy {
        stop_loss_condition: poc + 494.07,
        take_profit_conditions: vec![lst + 1_000.0, lst, lst - 500.0],
    };
    let p_and_l = x.compute_profit_and_losses(&s);
    dbg!(p_and_l);

    println!("poc resistance");
}
