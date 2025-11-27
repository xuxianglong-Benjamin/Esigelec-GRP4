"""
可视化组件
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from config import TECHNICAL_EXPLANATIONS, FUNDAMENTAL_EXPLANATIONS

class Visualizer:
    def __init__(self):
        self.technical_explanations = TECHNICAL_EXPLANATIONS
        self.fundamental_explanations = FUNDAMENTAL_EXPLANATIONS

    def create_price_chart(self, hist_data, company_name, color):
        """创建价格曲线图"""
        if hist_data.empty:
            return None
            
        fig = go.Figure()
        
        # 添加收盘价线
        fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data['Close'],
            mode='lines',
            name='Prix de Clôture',
            line=dict(color=color, width=2),
            hovertemplate='<b>%{x}</b><br>Prix: €%{y:.2f}<extra></extra>'
        ))
        
        # 添加移动平均线
        if len(hist_data) >= 20:
            ma_20 = hist_data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=ma_20,
                mode='lines',
                name='MM20',
                line=dict(color='orange', width=1, dash='dash'),
                opacity=0.7
            ))
        
        if len(hist_data) >= 50:
            ma_50 = hist_data['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=ma_50,
                mode='lines',
                name='MM50',
                line=dict(color='red', width=1, dash='dash'),
                opacity=0.7
            ))
        
        # 更新布局
        fig.update_layout(
            title=f"📈 Évolution du Prix de {company_name} (6 mois)",
            xaxis_title="Date",
            yaxis_title="Prix (€)",
            height=400,
            showlegend=True,
            hovermode='x unified',
            template="plotly_white"
        )
        
        return fig

    def create_score_gauge(self, score, title, color):
        """创建得分仪表盘"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 16}},
            number = {'suffix': "/5", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [None, 5], 'tickwidth': 1},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 2], 'color': "lightgray"},
                    {'range': [2, 3], 'color': "lightyellow"},
                    {'range': [3, 4], 'color': "lightgreen"},
                    {'range': [4, 5], 'color': "green"}
                ],
            }
        ))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        return fig

    def display_technical_analysis(self, result):
        """显示详细的技术分析"""
        st.markdown("---")
        st.subheader("🔧 Analyse Technique Détaillée")
        
        # 技术指标概览
        st.markdown("### 📊 Vue d'ensemble des Indicateurs Techniques")
        
        # 创建技术指标卡片
        tech_cols = st.columns(3)
        tech_indicators = ['rsi', 'moving_averages', 'macd']
        
        for idx, indicator in enumerate(tech_indicators):
            with tech_cols[idx]:
                score = result['detailed_scores']['technical'].get(indicator, 0)
                signal = result['technical_signals'].get(indicator, "N/A")
                explanation = self.technical_explanations.get(indicator, {})
                
                st.metric(
                    explanation.get('name', indicator),
                    f"{score}/5"
                )
                st.caption(signal)
        
        # 详细技术分析展开器
        with st.expander("📖 **ANALYSE TECHNIQUE COMPLÈTE**", expanded=True):
            
            # RSI详细分析
            st.markdown("#### 📈 Relative Strength Index (RSI)")
            rsi_value = result['metrics'].get('rsi', 50)
            rsi_explanation = self.technical_explanations['rsi']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Valeur RSI", f"{rsi_value}")
                st.progress(rsi_value/100, text=f"Position: {rsi_value}/100")
                
                # 修复RSI信号显示问题
                if rsi_value < 30:
                    st.success("**Zone de Survendu** - Signal d'achat potentiel")
                elif rsi_value > 70:
                    st.error("**Zone de Suracheté** - Signal de vente potentiel")
                else:
                    st.info("**Zone Neutre** - Aucun signal fort")
            
            with col2:
                st.markdown(rsi_explanation['detailed_explanation'])
                st.caption(f"**Stratégie**: {rsi_explanation['trading_strategy']}")
            
            st.markdown("---")
            
            # 移动平均线详细分析
            st.markdown("#### 📊 Moyennes Mobiles")
            ma_explanation = self.technical_explanations['moving_averages']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Prix Actuel", f"€{result['metrics']['current_price']:.2f}")
                st.metric("MA20", f"€{result['metrics']['ma_20']:.2f}")
                st.metric("MA50", f"€{result['metrics']['ma_50']:.2f}")
                
                golden_cross = result['metrics'].get('golden_cross', False)
                if golden_cross:
                    st.success("**✓ Croix d'Or confirmée**")
                else:
                    st.warning("**✗ Pas de Croix d'Or**")
            
            with col2:
                st.markdown(ma_explanation['detailed_explanation'])
                st.caption(f"**Signal actuel**: {result['technical_signals']['moving_averages']}")
            
            st.markdown("---")
            
            # MACD详细分析
            st.markdown("#### 🔄 MACD Analysis")
            macd_explanation = self.technical_explanations['macd']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ligne MACD", f"{result['metrics']['macd_line']:.4f}")
            with col2:
                st.metric("Ligne Signal", f"{result['metrics']['macd_signal']:.4f}")
            with col3:
                histogram_value = result['metrics']['macd_histogram']
                delta_direction = "📈 Hausse" if histogram_value > 0 else "📉 Baisse"
                st.metric("Histogramme", f"{histogram_value:.4f}", delta=delta_direction)
            
            st.markdown(macd_explanation['detailed_explanation'])
            st.caption(f"**Interprétation**: {result['technical_signals']['macd']}")
            
            st.markdown("---")
            
            # 布林带详细分析
            st.markdown("#### 📏 Bandes de Bollinger")
            bb_explanation = self.technical_explanations['bollinger_bands']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Position", f"{result['metrics']['bb_position']:.3f}")
                st.metric("Largeur", f"{result['metrics']['bb_width']}%")
                
                bb_position = result['metrics']['bb_position']
                if bb_position < 0.2:
                    st.success("**Près de la bande inférieure** - Opportunité")
                elif bb_position > 0.8:
                    st.error("**Près de la bande supérieure** - Prudence")
                else:
                    st.info("**Dans la bande moyenne** - Neutre")
            
            with col2:
                st.markdown(bb_explanation['detailed_explanation'])
                st.caption(f"**Volatilité**: {'Faible' if result['metrics']['bb_width'] < 8 else 'Élevée' if result['metrics']['bb_width'] > 20 else 'Normale'}")
            
            st.markdown("---")
            
            # 动量分析
            st.markdown("#### 🚀 Momentum des Prix")
            momentum_explanation = self.technical_explanations['momentum']
            
            momentum = result['metrics']['price_change_1m']
            st.metric("Variation sur 1 mois", f"{momentum}%")
            
            col1, col2 = st.columns(2)
            with col1:
                if momentum > 10:
                    st.success("**Forte accélération haussière**")
                elif momentum > 5:
                    st.info("**Momentum haussier modéré**")
                elif momentum > -5:
                    st.warning("**Momentum neutre**")
                elif momentum > -10:
                    st.error("**Momentum baissier modéré**")
                else:
                    st.error("**Forte pression baissière**")
            
            with col2:
                st.markdown(momentum_explanation['detailed_explanation'])

    def display_fundamental_analysis(self, result):
        """显示详细的基本面分析"""
        st.markdown("---")
        st.subheader("🏛️ Analyse Fondamentale Détaillée")
        
        # 基本面指标概览
        st.markdown("### 💼 Vue d'ensemble des Indicateurs Fondamentaux")
        
        # 创建基本面指标卡片
        fund_cols = st.columns(3)
        fund_indicators = ['pe_ratio', 'dividend_yield', 'roe']
        
        for idx, indicator in enumerate(fund_indicators):
            with fund_cols[idx]:
                score = result['detailed_scores']['fundamental'].get(indicator, 0)
                signal = result['fundamental_signals'].get(indicator, "N/A")
                explanation = self.fundamental_explanations.get(indicator, {})
                
                st.metric(
                    explanation.get('name', indicator),
                    f"{score}/5"
                )
                st.caption(signal)
        
        # 详细基本面分析展开器
        with st.expander("📊 **ANALYSE FONDAMENTALE COMPLÈTE**", expanded=True):
            
            # PER详细分析
            st.markdown("#### 💰 Ratio Prix/Bénéfice (PER)")
            pe_explanation = self.fundamental_explanations['pe_ratio']
            pe_value = result['metrics']['pe_ratio']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("PER", f"{pe_value:.1f}")
                
                if pe_value < 15:
                    st.success("**Sous-évalué** - Opportunité")
                elif pe_value < 25:
                    st.info("**Valorisation raisonnable**")
                else:
                    st.error("**Surévalué** - Risque")
            
            with col2:
                st.markdown(pe_explanation['detailed_explanation'])
                st.caption(f"**Conseil d'investissement**: {pe_explanation['investment_insight']}")
            
            st.markdown("---")
            
            # 股息率详细分析
            st.markdown("#### 💵 Rendement du Dividende")
            dividend_explanation = self.fundamental_explanations['dividend_yield']
            dividend_yield = result['metrics']['dividend_yield']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Rendement", f"{dividend_yield}%")
                if result['metrics']['dividend_rate'] > 0:
                    st.metric("Dividende par action", f"€{result['metrics']['dividend_rate']:.2f}")
                
                # 修复股息率显示逻辑
                if dividend_yield >= 5:
                    st.success("**Rendement très attractif**")
                elif dividend_yield >= 3:
                    st.info("**Rendement attractif**")
                elif dividend_yield >= 1.5:
                    st.warning("**Rendement modeste**")
                else:
                    st.error("**Rendement faible**")
            
            with col2:
                st.markdown(dividend_explanation['detailed_explanation'])
                st.caption(f"**Stratégie**: {dividend_explanation['investment_insight']}")
            
            st.markdown("---")
            
            # ROE详细分析
            st.markdown("#### 📈 Return on Equity (ROE)")
            roe_explanation = self.fundamental_explanations['roe']
            roe_value = result['metrics']['roe']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("ROE", f"{roe_value}%")
                
                if roe_value >= 15:
                    st.success("**Excellente rentabilité**")
                elif roe_value >= 10:
                    st.info("**Rentabilité correcte**")
                else:
                    st.error("**Rentabilité insuffisante**")
            
            with col2:
                st.markdown(roe_explanation['detailed_explanation'])
                st.caption("**Règle de Buffett**: ROE > 15% sur plusieurs années = entreprise de qualité")
            
            st.markdown("---")
            
            # 营收增长详细分析
            st.markdown("#### 🚀 Croissance du Chiffre d'Affaires")
            growth_explanation = self.fundamental_explanations['revenue_growth']
            growth_value = result['metrics']['revenue_growth']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Croissance CA", f"{growth_value}%")
                
                if growth_value >= 10:
                    st.success("**Forte croissance**")
                elif growth_value >= 5:
                    st.info("**Croissance modérée**")
                elif growth_value >= 0:
                    st.warning("**Croissance faible**")
                else:
                    st.error("**Récession**")
            
            with col2:
                st.markdown(growth_explanation['detailed_explanation'])
                st.caption("**Importance**: La croissance durable du CA est un signe de santé à long terme")
            
            st.markdown("---")
            
            # 负债率详细分析
            st.markdown("#### 🏦 Ratio Dette/Capitaux Propres")
            debt_explanation = self.fundamental_explanations['debt_to_equity']
            debt_value = result['metrics']['debt_to_equity']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Dette/Equity", f"{debt_value:.2f}")
                
                if debt_value <= 0.5:
                    st.success("**Faible endettement**")
                elif debt_value <= 1.0:
                    st.info("**Endettement modéré**")
                elif debt_value <= 2.0:
                    st.warning("**Endettement moyen**")
                elif debt_value <= 3.0:
                    st.error("**Endettement élevé**")
                else:
                    st.error("**Fort endettement**")
            
            with col2:
                st.markdown(debt_explanation['detailed_explanation'])
                st.caption("**Risque**: Un endettement excessif augmente la vulnérabilité aux hausses de taux d'intérêt")

    def display_news_analysis(self, company_name):
        """显示公司新闻分析"""
        st.markdown("---")
        st.subheader("📰 Analyse d'Actualités Récente")
        
        news_data = self.get_company_news(company_name)
        
        if news_data:
            # 显示新闻标题和来源
            st.markdown(f"**Titre :** {news_data['title']}")
            st.markdown(f"**Source :** {news_data['source']}")
            
            # 显示原新闻链接
            st.markdown(f"**Lien de l'article :** [📎 Accéder à l'article original]({news_data['url']})")
            
            # 新闻内容
            with st.expander("📖 Contenu de l'actualité"):
                st.write(news_data['content'])
            
            # 分析和评分
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("**🔍 Notre Analyse :**")
                st.write(news_data['analysis'])
            with col2:
                score = news_data['score']
                color = "green" if score >= 7 else "orange" if score >= 5 else "red"
                emoji = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                
                st.metric(
                    label=f"**Impact Score** {emoji}",
                    value=f"{score}/10",
                    delta="Positif" if score >= 7 else "Neutre" if score >= 5 else "Négatif"
                )
            
            st.markdown("**📋 Justification du score :**")
            st.write(news_data['justification'])
            
        else:
            st.info("📡 Aucune actualité récente disponible pour cette entreprise.")

    def get_company_news(self, company_name):
        """获取公司新闻数据 - 包含原新闻链接"""
        news_db = {
            "TOTAL Energie": {
                "title": "TotalEnergies démobilise son terminal méthanier flottant au Havre",
                "source": "Boursorama",
                "url": "https://www.boursorama.com/bourse/actualites/totalenergies-demobilise-son-terminal-methanier-flottant-au-havre-a7c37bd1c57493e0f668675a71ebbc3c?symbol=1rPTTE",
                "date": "Novembre 2024",
                "content": """TotalEnergies a annoncé la démobilisation de son terminal méthanier flottant au Havre. 
Cette installation, mise en service pendant la crise énergétique de 2022, n'est plus nécessaire 
compte tenu de la normalisation des approvisionnements en gaz naturel en Europe. Cette décision 
s'inscrit dans la stratégie d'optimisation des actifs du groupe.""",
                "analysis": """Cette décision reflète une gestion rationnelle des actifs. Bien que cela représente 
un désinvestissement, cela libère des ressources pour des projets plus stratégiques dans les 
énergies renouvelables et réduit les coûts d'exploitation inutiles. La démarche est positive 
car elle montre une adaptation rapide aux conditions de marché changeantes.""",
                "score": 7,
                "justification": """• Optimisation des coûts d'exploitation
• Recentrage sur les activités plus rentables
• Réallocation du capital vers la transition énergétique
• Impact financier positif à moyen terme
• Démontre une gestion agile des actifs"""
            },
            "Airbus": {
                "title": "Airbus parmi les valeurs à suivre aujourd'hui à Paris",
                "source": "Boursorama", 
                "url": "https://www.boursorama.com/bourse/actualites/airbus-bnp-paribas-casino-les-valesuivre-aujourd-hui-a-paris-eb3951d6d1ccc724346da17bddd44a32?symbol=1rPAIR",
                "date": "Novembre 2024",
                "content": """Airbus figure parmi les valeurs phares à surveiller sur la place de Paris aujourd'hui.
L'attention des investisseurs se porte sur les perspectives de commandes et la reprise du trafic aérien.
Le secteur aéronautique montre des signes de reprise soutenue après la période de crise.""",
                "analysis": """Être identifié comme une valeur à suivre indique un fort intérêt des investisseurs.
Cela peut refléter des attentes positives concernant les futures commandes d'avions ou des 
publications de résultats encourageantes. Cette visibilité est généralement bénéfique pour 
la liquidité et la valorisation de l'action.""",
                "score": 6,
                "justification": """• Visibilité accrue auprès des investisseurs
• Anticipation de nouvelles commandes
• Position dominante dans le secteur aéronautique
• Potentiel de performance positive
• Intérêt médiatique soutenu"""
            },
            "Dassault Systèmes": {
                "title": "Dassault Systèmes vers le test du plancher des 21,65€ du 16 mars 2020",
                "source": "Boursorama",
                "url": "https://www.boursorama.com/bourse/actualites/dassault-systemes-vers-le-test-du-plancher-des-21-65e-du-16-mars-2020-d3dfb380e879bd0f3d6def34da080974?symbol=1rPDSY",
                "date": "Mars 2024",
                "content": """L'action Dassault Systèmes s'approche de son niveau de support critique de 21,65€, 
un plancher technique datant de mars 2020. Les analystes surveillent ce niveau clé qui, 
s'il est franchi, pourrait entraîner une nouvelle vague de vente. La situation technique 
reste tendue pour le titre.""",
                "analysis": """La proximité d'un niveau de support technique important crée une situation délicate.
Une rupture de ce support pourrait entraîner une nouvelle vague de vente technique. 
Cette configuration reflète une pression vendeuse persistante et un manque de confiance 
des investisseurs à court terme.""",
                "score": 4,
                "justification": """• Signal technique négatif à court terme
• Risque de rupture du support clé
• Pression vendeuse potentielle
• Environnement technique défavorable
• Manque de dynamique haussière"""
            },
            "Hermès": {
                "title": "Hermès : chute de plus de 3%, vers 2.046€",
                "source": "Boursorama", 
                "url": "https://www.boursorama.com/bourse/actualites/hermes-chute-de-plus-de-3-vers-2-046e-248d19bd46cea2b0bdd8f15229855b58?symbol=1rPRMS",
                "date": "Novembre 2024",
                "content": """L'action Hermès a accusé une baisse de plus de 3% lors de la séance, 
s'établissant autour de 2.046€. Cette correction intervient dans un contexte de prises de bénéfices
après une forte performance récente. Le secteur du luxe dans son ensemble connaît une volatilité
accrue en cette période.""",
                "analysis": """Cette baisse reflète probablement des prises de bénéfices après une forte performance.
Les fondamentaux de l'entreprise restent solides, mais la valorisation était élevée.
Il s'agit probablement d'un mouvement technique plutôt que d'un changement structurel
dans les fondamentaux de l'entreprise.""",
                "score": 5,
                "justification": """• Prise de bénéfices technique probable
• Valorisation antérieure élevée justifiant une correction
• Fondamentaux de l'entreprise restant solides
• Opportunité d'achat potentielle à moyen terme
• Volatilité normale sur les titres de croissance"""
            },
            "Sopra Steria": {
                "title": "Sopra Steria annonce un partenariat stratégique entre CNN MCO, Thales et CS Group",
                "source": "Boursorama",
                "url": "https://www.boursorama.com/bourse/actualites/sopra-steria-annonce-un-partenariat-strategique-entre-cnn-mco-thales-et-cs-group-e0222f771fa182f6e95b1df1dcfdfac7?symbol=1rPSOP",
                "date": "Novembre 2024", 
                "content": """Sopra Steria a officialisé un partenariat stratégique majeur avec plusieurs acteurs 
du secteur pour renforcer son positionnement dans les solutions digitales et la cybersécurité.
Ce partenariat vise à développer des offres communes et à capitaliser sur les complémentarités
technologiques des différents partenaires.""",
                "analysis": """Ce partenariat stratégique pourrait ouvrir de nouvelles opportunités commerciales
et renforcer la position de Sopra Steria dans des secteurs porteurs comme la cybersécurité
et la transformation digitale. Les synergies entre les partenaires pourraient générer
des revenus supplémentaires à moyen terme.""",
                "score": 8,
                "justification": """• Accès à de nouveaux marchés et clients
• Renforcement des compétences techniques
• Effets de synergie potentiels importants
• Amélioration de la compétitivité à long terme
• Positionnement renforcé dans les secteurs porteurs"""
            }
        }
        
        return news_db.get(company_name)

    def display_welcome(self):
        """显示欢迎界面"""
        from config import COMPANIES, TEAM_MEMBERS
        
        st.markdown("""
        ## 🎯 Bienvenue dans le Système d'Analyse Boursière Complète
        
        Ce projet analyse 5 entreprises françaises du CAC 40 en utilisant une approche complète:
        
        ### 🔧 **Analyse Technique Avancée**
        - 📈 RSI, MACD, Moyennes Mobiles
        - 📏 Bandes de Bollinger, Momentum
        - 🚀 Signaux de trading détaillés
        
        ### 🏛️ **Analyse Fondamentale Approfondie**  
        - 💰 PER, Rendement Dividende, ROE
        - 🚀 Croissance du Chiffre d'Affaires
        - 🏦 Structure financière et endettement
        
        ### 📋 **Entreprises Couvertes**:
        """)
        
        # 显示所有公司卡片
        cols = st.columns(5)
        for idx, (company, info) in enumerate(COMPANIES.items()):
            with cols[idx]:
                member = TEAM_MEMBERS[company]
                st.markdown(f"""
                <div style='background-color: {info["color"]}20; padding: 15px; border-radius: 10px; border-left: 4px solid {info["color"]};'>
                    <h4 style='margin: 0;'>{company}</h4>
                    <p style='margin: 5px 0; font-size: 12px;'>{info['description']}</p>
                    <p style='margin: 0; font-size: 11px; color: gray;'>👤 {member}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("💡 **Instructions**: Sélectionnez une entreprise dans la barre latérale et cliquez sur 'Lancer l'Analyse'")

    def display_analysis_result(self, result):
        """显示完整分析结果"""
        # 头部信息
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"# {result['company_name']} ({result['ticker']})")
            st.markdown(f"**Secteur**: {result['description']}")
            st.markdown(f"**Analyste**: 👤 {result['team_member']}")
        
        with col2:
            st.metric("💰 Prix Actuel", f"€{result['current_price']:.2f}")
        
        with col3:
            st.metric("📅 Dernière Analyse", result['timestamp'].split()[0])
        
        st.markdown("---")
        
        # 添加价格曲线图
        if not result['hist_data'].empty:
            price_chart = self.create_price_chart(
                result['hist_data'], 
                result['company_name'],
                result['color']
            )
            if price_chart:
                st.plotly_chart(price_chart, use_container_width=True)
                st.markdown("---")
        
        # 推荐卡片
        rec_color = "green" if "ACHAT" in result['recommendation'] else \
                   "orange" if "SURVEILLER" in result['recommendation'] else \
                   "yellow" if "NE RIEN FAIRE" in result['recommendation'] else "red"
        
        st.markdown(f"""
        <div style='background-color: {rec_color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {rec_color}; margin: 20px 0;'>
            <h2 style='margin: 0; color: {rec_color};'>{result['recommendation']}</h2>
            <p style='margin: 10px 0 0 0; font-size: 16px;'>{result['justification']}</p>
            <p style='margin: 5px 0 0 0; font-size: 14px; color: gray;'>Score Total: {result['total_score']}/5.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 得分仪表盘
        st.subheader("🎯 Scores d'Analyse")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(
                self.create_score_gauge(
                    result['fundamental_score'], 
                    "Score Fondamental", 
                    "blue"
                ), 
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                self.create_score_gauge(
                    result['technical_score'], 
                    "Score Technique", 
                    "orange"
                ), 
                use_container_width=True
            )
        
        with col3:
            st.plotly_chart(
                self.create_score_gauge(
                    result['total_score'], 
                    "Score Total", 
                    "green"
                ), 
                use_container_width=True
            )
        
        # 显示详细分析
        self.display_fundamental_analysis(result)
        self.display_technical_analysis(result)
        
        # 添加新闻分析部分
        self.display_news_analysis(result['company_name'])