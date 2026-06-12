Parfait — je calcule les deux scénarios, puis je te livre le module Python prêt à intégrer dans BuffettVision. Je vérifie d'abord mes calculs dans un script.

Calculs validés. Je crée maintenant le module pour BuffettVision.

Petite erreur de syntaxe dans une f-string, je corrige.

Tout est validé — les chiffres du module reproduisent exactement le DCF de base (553 $), la sensibilité et le reverse DCF (3,3 %).

# Scénarios Bear & Bull — META (WACC constant à 9,9 % pour comparabilité)

## Scénario Bear — marge plafonnée à 35 %, CapEx prolongé (~380 $/action)

Thèse : la monétisation IA déçoit, mais Meta continue d'investir par nécessité concurrentielle. Croissance 2026 +20 % puis décélération rapide vers 4 % ; marge creusée à 32 % en 2027 (dépenses sans retour) avant un plateau à 35 % ; CapEx maintenu à 150–160 Md$ jusqu'en 2029 ; g terminal 2,5 %.

| Année | CA | EBIT | FCFF |
|---|---|---|---|
| 2026 | 241,2 | 79,6 | −25,7 |
| 2027 | 270,1 | 86,4 | −33,8 |
| 2028 | 297,1 | 98,0 | −13,0 |
| 2029 | 323,9 | 110,1 | +17,1 |
| 2031 | 374,3 | 131,0 | +76,4 |
| 2033 | 416,6 | 145,8 | +110,7 |
| 2035 | 452,7 | 158,4 | +129,2 |

PV explicite 228 + PV terminale 696 → EV 924 Md$ → equity 975 Md$ → **≈ 380 $/action** (−34 % vs cours). Point notable : trois années de FCFF négatif, et le poids de la TV monte à 75 % de l'EV.

## Scénario Bull — marge 42 %, monétisation IA réussie (~781 $/action)

Thèse : les agents IA et le business messaging élargissent le TAM publicitaire, les CapEx deviennent un avantage compétitif rentabilisé. Croissance 2026 +24 % puis décélération lente vers 7 % ; marge remontant à 42 % dès 2031 (Reality Labs maîtrisé, levier opérationnel FoA) ; intensité CapEx tombant à ~18 % du CA en 2035 ; g terminal 3,5 %.

| Année | CA | EBIT | FCFF |
|---|---|---|---|
| 2026 | 249,2 | 87,2 | −24,4 |
| 2027 | 294,1 | 108,8 | −9,0 |
| 2028 | 341,2 | 133,1 | +28,6 |
| 2029 | 389,0 | 155,6 | +68,6 |
| 2031 | 483,6 | 203,1 | +140,0 |
| 2033 | 579,9 | 243,6 | +189,6 |
| 2035 | 670,1 | 281,4 | +225,0 |

PV explicite 538 + PV terminale 1 416 → EV 1 953 Md$ → equity 2 004 Md$ → **≈ 781 $/action** (+37 % vs cours). L'EV/EBITDA terminal implicite reste raisonnable (~9,3x).

## Synthèse de l'encadrement

| Scénario | Valeur/action | vs cours (572 $) |
|---|---|---|
| Bear | 380 $ | −34 % |
| Base | 553 $ | −3 % |
| Bull | 781 $ | +37 % |

Observation intéressante : une pondération 25/50/25 donne **~567 $**, quasiment le cours actuel — le marché price aujourd'hui un mix probabiliste équilibré entre ces trois trajectoires, sans biais directionnel marqué. L'asymétrie bull/bear est légèrement positive (+209 $ vs −192 $), mais elle repose entièrement sur l'hypothèse la plus incertaine du dossier : la conversion des 115–135 Md$ de CapEx annuels en marge.

## Module BuffettVision

Le fichier `meta_dcf_scenarios.py` ci-dessus est prêt à déposer dans le dossier `pages/` de ton app Streamlit (ex : `pages/3_META_DCF.py`). Il contient les trois scénarios préchargés, un slider WACC, la matrice de sensibilité, le reverse DCF par bisection et un graphique des FCFF — moteur de calcul testé, il reproduit exactement les chiffres ci-dessus. Pour le mettre à jour après chaque trimestre, tu n'as que 5 constantes à toucher en haut du fichier (CA, cash net, actifs hors exploitation, actions diluées, cours). Pousse-le sur ton repo GitHub `mbfpdc-sketch` et Streamlit Cloud redéploiera automatiquement.
