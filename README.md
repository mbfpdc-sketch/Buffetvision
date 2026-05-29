# 🏦 BuffettVision – L'Investisseur Patient

> *« Le prix est ce que vous payez. La valeur est ce que vous obtenez. »* — Warren Buffett

Application web d'analyse d'actions dans le **pur style Warren Buffett** : valeur intrinsèque, marge de sécurité, moat économique et recommandation claire en français.

---

## ✨ Fonctionnalités

| Section | Contenu |
|---------|---------|
| 🔍 Recherche | Ticker OU nom d'entreprise (AAPL, Apple, KO, Coca-Cola, MC.PA…) |
| 📈 Graphique | Prix interactif 1 an / 5 ans / Max avec moyenne mobile |
| 💰 Santé financière | CA, Bénéfice net, FCF sur 10 ans + 9 ratios clés |
| 🏰 Moat & Score | Checklist Buffett automatique + Buffett Score 0-100 |
| 🎯 Valeur intrinsèque | DCF simplifié (Owner Earnings) avec hypothèses modulables |
| 🏆 Recommandation | Verdict clair : Excellent achat / Surveiller / Éviter |
| ⚠️ Risques | Risques spécifiques à l'entreprise + secteur |
| 📰 Actualités | 5 dernières news via yfinance |
| 📄 Export PDF | Rapport complet téléchargeable |

---

## 🚀 Lancement en 30 secondes

### 1. Cloner / Télécharger
```bash
# Si vous avez git :
git clone <votre-repo>
cd buffettvision

# Ou simplement créez un dossier et copiez app.py + requirements.txt dedans
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvre automatiquement sur **http://localhost:8501** 🎉

---

## ☁️ Déploiement gratuit sur Streamlit Cloud (1 clic)

1. Poussez votre code sur GitHub (dépôt public ou privé)
2. Allez sur [share.streamlit.io](https://share.streamlit.io)
3. Connectez votre compte GitHub
4. Sélectionnez votre dépôt et `app.py`
5. Cliquez **Deploy** → URL publique en 2 minutes !

---

## 🎯 Comment utiliser BuffettVision

### Recherche
Tapez dans la barre de recherche :
- Un **ticker** : `AAPL`, `KO`, `BRK-B`, `MC.PA`, `NESN.SW`
- Un **nom** : `Apple`, `Coca-Cola`, `Berkshire`, `LVMH`
- Cliquez sur une **suggestion rapide** en dessous de la barre

### Clé API FMP (optionnel)
Sans clé API, yfinance fournit des données de très bonne qualité (gratuitement).  
Si vous souhaitez des données encore plus précises (bilans détaillés, flux de trésorerie historiques plus complets), obtenez une clé gratuite sur [financialmodelingprep.com](https://financialmodelingprep.com) et entrez-la dans le champ prévu.

### Modèle DCF
Les paramètres du DCF sont **modifiables en temps réel** :
- **Taux de croissance (5 premières années)** : soyez conservateur (5-8%)
- **Taux de croissance (années 6-10)** : ralentissement naturel (3-5%)
- **Taux d'actualisation** : rendement minimum exigé, Buffett utilise ~9-10%
- **Croissance perpétuelle** : taux terminal (2-3% = inflation long terme)

---

## 🏗️ Architecture du projet

```
buffettvision/
├── app.py              # Application principale (tout-en-un)
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

Le code est volontairement **monofichier** pour faciliter le déploiement sur Streamlit Cloud.

---

## 📦 Dépendances

| Package | Usage |
|---------|-------|
| `streamlit` | Framework web |
| `yfinance` | Données financières (gratuit, sans clé) |
| `pandas` | Manipulation des données |
| `numpy` | Calculs numériques |
| `plotly` | Graphiques interactifs |
| `reportlab` | Export PDF |
| `requests` | Requêtes HTTP |

---

## ⚠️ Avertissement légal

BuffettVision est un outil éducatif. Les analyses et recommandations produites sont **automatiques et basées sur des algorithmes**. Elles ne constituent **pas un conseil en investissement**.  
Faites toujours votre propre recherche (DYOR) avant d'investir. Les performances passées ne préjugent pas des performances futures.

---

## 💡 Inspiré de

- La philosophie d'investissement de **Warren Buffett** et **Charlie Munger**
- Le livre *The Intelligent Investor* de **Benjamin Graham**
- Les lettres annuelles aux actionnaires de **Berkshire Hathaway**

---

*Made with ❤️ and Python · Interface entièrement en français*
