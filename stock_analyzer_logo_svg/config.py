"""
配置文件和常量定义
"""

# 公司配置
COMPANIES = {
    "TOTAL Energie": {
        "ticker": "TTE.PA",
        "color": "#FF6B35",
        "description": "Énergie - Pétrole et Gaz"
    },
    "Hermès": {
        "ticker": "RMS.PA", 
        "color": "#E6B89C",
        "description": "Luxe - Maroquinerie et Mode"
    },
    "Airbus": {
        "ticker": "AIR.PA",
        "color": "#00A8E8", 
        "description": "Aérospatiale - Aviation"
    },
    "Dassault Systèmes": {
        "ticker": "DSY.PA",
        "color": "#0052CC",
        "description": "Technologie - Logiciels 3D"
    },
    "Sopra Steria": {
        "ticker": "SOP.PA",
        "color": "#6A4C93",
        "description": "Services IT - Conseil"
    }
}

# 团队成员分配
TEAM_MEMBERS = {
    "TOTAL Energie": "Mathys",
    "Hermès": "Ismael", 
    "Airbus": "XU",
    "Dassault Systèmes": "Pierre",
    "Sopra Steria": "Yann"
}

# 技术指标详细解释
TECHNICAL_EXPLANATIONS = {
    "rsi": {
        "name": "Relative Strength Index (RSI)",
        "description": "Oscillateur de momentum qui mesure la vitesse et l'amplitude des mouvements de prix",
        "detailed_explanation": """
        Le RSI compare les gains récents aux pertes récentes pour déterminer les conditions de surachat et de survendu.
        - **Calcul**: RSI = 100 - (100 / (1 + RS)) où RS = (Gain moyen sur 14 périodes / Perte moyenne sur 14 périodes)
        - **Période standard**: 14 jours
        - **Utilité**: Identifier les points de retournement et confirmer les tendances
        """,
        "interpretation": {
            "0-30": "🟢 Zone de survendu - Potentiel d'achat (RSI < 30)",
            "30-70": "⚪ Zone neutre - Aucun signal fort",
            "70-100": "🔴 Zone de surachat - Potentiel de vente (RSI > 70)"
        },
        "trading_strategy": "Acheter quand RSI < 30 (avec confirmation), vendre quand RSI > 70"
    },
    "moving_averages": {
        "name": "Moyennes Mobiles (MM)",
        "description": "Indicateur de tendance qui lisse les fluctuations de prix",
        "detailed_explanation": """
        Les moyennes mobiles identifient la direction de la tendance et fournissent des niveaux de support/résistance.
        - **MM20**: Tendance à court terme (1 mois)
        - **MM50**: Tendance à moyen terme (2.5 mois)  
        - **MM200**: Tendance à long terme (10 mois)
        - **Croix d'Or**: MM20 croise au-dessus de MM50 (signal haussier)
        - **Croix de la Mort**: MM20 croise sous MM50 (signal baissier)
        """,
        "interpretation": {
            "bullish": "🟢 Prix > MM20 > MM50 > MM200 - Forte tendance haussière",
            "neutral_bullish": "🟡 Prix > MM20, MM20 > MM50 - Tendance haussière",
            "neutral": "⚪ Configuration mixte - Tendance incertaine",
            "neutral_bearish": "🟠 Prix < MM20, MM20 < MM50 - Tendance baissière",
            "bearish": "🔴 Prix < MM20 < MM50 < MM200 - Forte tendance baissière"
        },
        "trading_strategy": "Acheter sur croix d'or, vendre sur croix de la mort"
    },
    "macd": {
        "name": "MACD (Moving Average Convergence Divergence)",
        "description": "Oscillateur de tendance qui montre la relation entre deux moyennes mobiles exponentielles",
        "detailed_explanation": """
        Le MACD se compose de trois éléments:
        - **Ligne MACD**: EMA(12) - EMA(26) - Mesure le momentum
        - **Ligne de signal**: EMA(9) du MACD - Ligne de déclenchement
        - **Histogramme**: MACD - Signal - Force du momentum
        
        **Signaux importants**:
        - Croisement au-dessus de la ligne de signal: Achat
        - Croisement sous de la ligne de signal: Vente  
        - Divergence haussière/baissière: Signaux avancés
        """,
        "interpretation": {
            "strong_bullish": "🟢 MACD > Signal > 0 - Fort momentum haussier",
            "bullish": "🟡 MACD > Signal - Signal haussier",
            "neutral": "⚪ MACD ≈ Signal - Point d'inflexion",
            "bearish": "🟠 MACD < Signal - Signal baissier",
            "strong_bearish": "🔴 MACD < Signal < 0 - Fort momentum baissier"
        },
        "trading_strategy": "Acheter sur croisement haussier, vendre sur croisement baissier"
    },
    "bollinger_bands": {
        "name": "Bandes de Bollinger",
        "description": "Enveloppes de volatilité qui s'adaptent aux conditions de marché",
        "detailed_explanation": """
        Les Bandes de Bollinger mesurent la volatilité relative:
        - **Bande moyenne**: SMA(20) - Tendance centrale
        - **Bande supérieure**: SMA(20) + 2 × Écart-type(20)
        - **Bande inférieure**: SMA(20) - 2 × Écart-type(20)
        
        **Concepts clés**:
        - **Compression**: Faible volatilité (bandes resserrées) - Préparation à un mouvement important
        - **Expansion**: Haute volatilité (bandes élargies) - Mouvement en cours
        - **Rebond**: Prix rebondit sur les bandes - Retour à la moyenne
        """,
        "interpretation": {
            "oversold": "🟢 Prix près bande inférieure - Survendu potentiel",
            "neutral_low": "🟡 Prix dans tiers inférieur - Léger survendu",
            "neutral": "⚪ Prix dans bande moyenne - Neutre",
            "overbought_high": "🟠 Prix dans tiers supérieur - Léger surachat",
            "overbought": "🔴 Prix près bande supérieure - Suracheté potentiel"
        },
        "trading_strategy": "Acheter près bande inférieure, vendre près bande supérieure"
    },
    "momentum": {
        "name": "Momentum des Prix",
        "description": "Mesure le taux de changement des prix sur une période donnée",
        "detailed_explanation": """
        Le momentum évalue la vitesse des mouvements de prix:
        - **Période**: 1 mois (22 jours de bourse)
        - **Calcul**: ((Prix actuel - Prix il y a 1 mois) / Prix il y a 1 mois) × 100%
        - **Importance**: Identifie l'accélération ou le ralentissement des tendances
        
        **Utilisation**:
        - Momentum positif croissant: Tendance se renforce
        - Momentum positif décroissant: Tendance s'affaiblit
        - Momentum négatif: Correction en cours
        """,
        "interpretation": {
            "very_strong_bullish": "🟢 > +15% - Forte accélération haussière",
            "strong_bullish": "🟡 +8% à +15% - Bon momentum haussier",
            "neutral": "⚪ -5% à +8% - Momentum neutre",
            "bearish": "🟠 -8% à -5% - Momentum baissier modéré",
            "very_bearish": "🔴 < -8% - Fort momentum baissier"
        },
        "trading_strategy": "Suivre la direction du momentum pour confirmer les tendances"
    }
}

# 基本面指标详细解释
FUNDAMENTAL_EXPLANATIONS = {
    "pe_ratio": {
        "name": "Ratio Prix/Bénéfice (PER)",
        "description": "Mesure combien les investisseurs sont prêts à payer pour 1€ de bénéfice",
        "detailed_explanation": """
        Le PER est l'un des ratios de valorisation les plus utilisés:
        - **Calcul**: Prix de l'action / Bénéfice par action (EPS)
        - **PER trailing**: Basé sur les bénéfices passés
        - **PER forward**: Basé sur les bénéfices futurs estimés
        
        **Interprétation par secteur**:
        - Technologie: PER élevé (croissance attendue)
        - Énergie: PER modéré (stabilité)
        - Luxe: PER variable (qualité des bénéfices)
        """,
        "interpretation": {
            "undervalued": "🟢 PER < 15 - Potentiellement sous-évalué",
            "fair_value": "🟡 PER 15-25 - Valorisation raisonnable", 
            "overvalued": "🔴 PER > 25 - Potentiellement surévalué"
        },
        "investment_insight": "Comparer le PER avec la moyenne du secteur et la croissance des bénéfices"
    },
    "dividend_yield": {
        "name": "Rendement du Dividende",
        "description": "Pourcentage du prix de l'action versé aux actionnaires sous forme de dividendes",
        "detailed_explanation": """
        Le rendement dividendes indique le revenu généré par l'investissement:
        - **Calcul**: (Dividende annuel par action / Prix de l'action) × 100%
        - **Paiement**: Trimestriel, semestriel ou annuel
        - **Croissance**: Augmentation régulière des dividendes = entreprise saine
        
        **Stratégies**:
        - **Dividend Investing**: Recherche de rendements stables
        - **Dividend Growth**: Recherche de croissance des dividendes
        """,
        "interpretation": {
            "high_yield": "🟢 > 5% - Rendement très attractif",
            "good_yield": "🟡 3-5% - Rendement attractif",
            "modest_yield": "⚪ 1.5-3% - Rendement modeste",
            "low_yield": "🟠 0.5-1.5% - Rendement faible",
            "no_yield": "🔴 < 0.5% - Peu attractif pour revenus"
        },
        "investment_insight": "Évaluer la soutenabilité du dividende (payout ratio)"
    },
    "roe": {
        "name": "Return on Equity (ROE)",
        "description": "Mesure la rentabilité des capitaux propres investis",
        "detailed_explanation": """
        Le ROE montre l'efficacité avec laquelle la direction utilise les fonds des actionnaires:
        - **Calcul**: (Bénéfice net / Capitaux propres) × 100%
        - **Importance**: Indicateur clé de la qualité managériale
        - **Règle de Buffett**: ROE > 15% sur plusieurs années = entreprise de qualité
        
        **Analyse DuPont**:
        ROE = Marge nette × Rotation actif × Levier financier
        """,
        "interpretation": {
            "excellent": "🟢 > 20% - Excellente rentabilité",
            "good": "🟡 15-20% - Bonne rentabilité", 
            "average": "⚪ 10-15% - Rentabilité moyenne",
            "poor": "🔴 < 10% - Faible rentabilité"
        },
        "investment_insight": "Rechercher un ROE stable ou croissant sur plusieurs années"
    },
    "revenue_growth": {
        "name": "Croissance du Chiffre d'Affaires",
        "description": "Taux de croissance des ventes de l'entreprise",
        "detailed_explanation": """
        La croissance du CA reflète la capacité de l'entreprise à développer son activité:
        - **Calcul**: ((CA actuel - CA précédent) / CA précédent) × 100%
        - **Période**: Généralement annuelle ou trimestrielle
        - **Importance**: Indicateur de demande pour les produits/services
        
        **Types de croissance**:
        - Croissance organique: Ventes existantes
        - Croissance par acquisition: Achats d'entreprises
        """,
        "interpretation": {
            "high_growth": "🟢 > 15% - Forte croissance",
            "good_growth": "🟡 8-15% - Croissance saine",
            "stable": "⚪ 0-8% - Croissance modérée", 
            "declining": "🔴 < 0% - Déclin des ventes"
        },
        "investment_insight": "La croissance durable du CA est un signe de santé à long terme"
    },
    "debt_to_equity": {
        "name": "Ratio Dette/Capitaux Propres",
        "description": "Mesure le levier financier et le risque de solvabilité",
        "detailed_explanation": """
        Ce ratio évalue la structure financière de l'entreprise:
        - **Calcul**: Dette totale / Capitaux propres
        - **Contexte**: Varie selon le secteur d'activité
        - **Risque**: Trop de dette = vulnérabilité aux hausses de taux
        
        **Par secteur**:
        - Industrie lourde: Ratio plus élevé acceptable
        - Technologie: Ratio faible préférable
        """,
        "interpretation": {
            "low_risk": "🟢 < 0.5 - Faible endettement",
            "moderate_risk": "🟡 0.5-1.0 - Endettement modéré",
            "medium_risk": "⚪ 1.0-2.0 - Endettement moyen",
            "high_risk": "🟠 2.0-3.0 - Endettement élevé",
            "very_high_risk": "🔴 > 3.0 - Fort endettement"
        },
        "investment_insight": "Évaluer la capacité de remboursement et le coût de la dette"
    }
}