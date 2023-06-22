# Uttak av NVDB-data for inntekstberegning fylkesveg for statsbudsjett 2024

Vi viser til regjeringsdokumentet 
[Forslag til ny modell for beregning av kriteriet for fylkesveg i inntektssystemet for fylkeskommunene](https://www.regjeringen.no/no/dokumenter/forslag-til-ny-modell-for-beregning-av-kriteriet-for-fylkesveg-i-inntektssystemet-for-fylkeskommunene/id2864850/), som igjen viser til [denne rapporten](https://www.regjeringen.no/contentassets/e8645ebe0e02470da89253caef0addba/rapport-forenklet-modell-til-kriteriet-for-utgiftsbehov-ti1405835.pdf). Denne rapporten, skrevet av konsulentselskapet Vianova, har detaljerte instruksjoner for hvilke data som inngår i inntektsmodellen, samt detaljerte instruksjoner for nedlasting og databearbeiding. Disse instruksjonene er her omsatt til python-kode for automatisert, repeterbar og etterprøvbar fremstiling. Rapporten er også 
[lagret lokalt](./bilder/rapport-forenklet-modell-til-kriteriet-for-utgiftsbehov-ti1405835.pdf)

Den formelle bestillingen for budsjettåret 2024 er lagt i mappen [bestilling](./bestilling/). Her er det en del endriner i uttak fra ferjedatabanken, mens datauttak fra NVDB og Brutus følger samme metodikk som i fjor. 

### Ny fylkesstruktur 2024

Fylkene _30 Viken_, _38 Vestfold og Telemark_ samt _54 Troms og Finnmark_ deles opp i de 7 nye fylkene: 
  * 31 Østfold
  * 32 Akershus
  * 33 Buskerud
  * 39 Vestfold
  * 40 Telemark
  * 55 Troms
  * 56 Finnmark

Oversettelse fra 2023 kommunenummer til 2024 fylkesnummer er beskrevet i dokumentet [20_73300-13 Skjema for grunnlagsdata til fylkesvegkriteriet  21460343_1_1.pdf](./bestilling/20_73300-13_Bestilling_av_kriteriedata_til_inntektssystemet_til_fylkeskommunene_21460341_1_1.pdf). Denne tabellen er oversatt til semikolon-separert CSV [nyFylkesinndeling.csv](./kode/nyFylkesinndeling.csv), og vi har laget funksjonen `lastnedvegnett.py/fylker2024` som oversetter fra 2023-kommuner til 2024-fylker for en (geo)pandas (geo)dataframe. 

# Fremgangsmåte og parametre 

Parametrene med tilhørende datakilde og pythonscript er vist i tabellen under. Hvert script produserer to regneark i mappen `/resultater`, ett regneark aggregert med 2023-fylker og ett med 2024-fylker.  2023-regnearkene brukes til å sammenligne med fjorårets leveranse. 

| parameter                                        | Datkilde                             | Resultatfil               | Python script                 |
| ------------------------------------------------ |  ----------------------------------- | ------------------------- | -----------------------------|
| Lengde vegnett (km)                              | nvdb api                             |veglengerFVJuni2023.xlsx   | script_rapport01_fylkesveg.py |
| Lengde vegnett som har ÅDT-data (km)             | nvdb api                             | ÅDTanalyse.xlsx           | script_AADT_trafikkarbeid.py  |     
| Feltlengde (km)                                  | nvdb api                             | veglengerFVJuni2023.xlsx  | script_rapport01_fylkesveg.py |     
| Trafikkarbeid (mill kjtkm/døgn)                  | nvdb api                             | ÅDTanalyse.xlsx           | script_AADT_trafikkarbeid.py  |
| Veglengde med ÅDT > 4000 (km)                    | nvdb api                             | ÅDTanalyse.xlsx           | script_AADT_trafikkarbeid.py  |
| Veglengde med ÅDT > 1500 (km)                    | nvdb api                             | ÅDTanalyse.xlsx           | script_AADT_trafikkarbeid.py  |
| Rekkverk (lm)                                    | nvdb api                             | rekkverk.xlsx             | script_rekkverk.py            |
| Lyspunkt i dagen (antall)                        | nvdb api                             | belysningspunkt.xlsx      | script_belysningspunkt.py     |
| Lengde ikke-undersjøiske tunnelløp (m)           | nvdb api                             | tunneler.xlsx             | script_tunnelanalyse.py       |
| Lengde undersjøiske tunnelløp (m)                | nvdb api                             | tunneler.xlsx             | script_tunnelanalyse.py       |
| Lengde bruer av stål (m)                         | 160623 grunnlagsdata bruer.xlsx      | bruer_ferjekaier.xlsx     | script_bruer_og_ferjekai.py   |
| Lengde bruer av andre materialtyper enn stål (m) | 140623 grunnlagsdata ferjekaier.xlsx | bruer_ferjekaier.xlsx     | script_bruer_og_ferjekai.py   |
| Ferjekaibruer og tillegskaier (antall)           | nvdb api                             | ferjekai.xlsx             | script_bruer_og_ferjekai.py   |
| G/S veglengde                                    | nvdb api                             | sykkelveg.xlsx            | script_rapport21_gangsykkel.py   |
| Veg med fartsgrense 50 km/t eller lavere (km)    | nvdb api                             | fartMax50kmt.xlsx         | script_rapport07_fart_u50.py |


### Sluttleveranse

Pythonscriptet `sluttproduksjon.py` leser resultat-regnearkene og skjøter sammen data i regnearket `Grunnlagsdata-inntekt-Fylkeskommunene2024.xlsx`, som er vår endelige leveranse. 

# Sammenligning med fjoråret

For å sammenligne med fjorårets statsbudsjett-leveranse har vi også aggregert data etter 2023-fylkesinndelingen. Disse regenarkene har `verifiser` i filnavnet. Scriptet `verifiserLeveranse.py` sammenstiller fjorårets leveranse (_Grunnlagsdata-inntekt-fylkeskommune2023.xlsx_) med ferske tall per juni 2023, lagret til regnearket `_verifiserMotifjor.xlsx`. Bortsett fra fylkesinndelingen er metodikken identisk for 2024-leveransen og denne verifiseringsrutinen. 

# Generelle betraktninger

Rutinen med at samferdselsdepartementet "_bestiller_" via formelle brev til vegdirektoratet og derfra til SVV avdelig "_Transport og samfunn_" gir veldig stor avstand mellom behov og utfører. Dette er uheldig og inviterer til misforståelser. I stedet anbefaler vi å gjennomføre felles workshop eller tilsvarende, der vi får avklart felles begreper og diskutert uklarheter i bestilling, datainnhold og så videre. 

