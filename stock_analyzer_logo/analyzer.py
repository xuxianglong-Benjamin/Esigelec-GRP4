"""
主要分析逻辑
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

from config import COMPANIES, TEAM_MEMBERS, TECHNICAL_EXPLANATIONS, FUNDAMENTAL_EXPLANATIONS

class StockAnalyzer:
    def __init__(self):
        self.companies = COMPANIES
        self.team_members = TEAM_MEMBERS
        self.technical_explanations = TECHNICAL_EXPLANATIONS
        self.fundamental_explanations = FUNDAMENTAL_EXPLANATIONS

    def get_stock_data(self, ticker):
        """获取股票数据"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="6mo")
            
            return {
                'info': info,
                'hist': hist,
                'success': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def calculate_technical_indicators(self, hist_data):
        """计算完整的技术指标"""
        if hist_data.empty or len(hist_data) < 50:
            return {'total_score': 0, 'detailed_scores': {}, 'metrics': {}, 'signals': {}}
        
        scores = {}
        signals = {}
        detailed_metrics = {}
        
        try:
            current_price = hist_data['Close'].iloc[-1]
            
            # 1. RSI计算
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1] if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50
            
            # RSI评分和信号 - 修复版本
            if current_rsi < 30:
                rsi_score = 5
                rsi_signal = "🟢 FORT SURVENDU - Signal d'achat potentiel"
            elif current_rsi < 40:
                rsi_score = 4  
                rsi_signal = "🟡 SURVENDU - Opportunité d'achat modérée"
            elif current_rsi < 60:
                rsi_score = 3
                rsi_signal = "⚪ NEUTRE - Pas de signal directionnel clair"
            elif current_rsi < 70:
                rsi_score = 2
                rsi_signal = "🟠 SURACHETÉ - Prudence recommandée"
            else:
                rsi_score = 1
                rsi_signal = "🔴 FORT SURACHETÉ - Signal de vente potentiel"
            
            scores['rsi'] = rsi_score
            signals['rsi'] = rsi_signal
            detailed_metrics['rsi'] = round(current_rsi, 1)
            
            # 2. 移动平均线计算
            ma_20 = hist_data['Close'].rolling(window=20).mean().iloc[-1]
            ma_50 = hist_data['Close'].rolling(window=50).mean().iloc[-1]
            ma_200 = hist_data['Close'].rolling(window=200).mean().iloc[-1] if len(hist_data) >= 200 else ma_50
            
            # 移动平均线评分和信号
            if current_price > ma_20 > ma_50 > ma_200:
                ma_score = 5
                ma_signal = "🟢 FORTE TENDANCE HAUSSIÈRE - Configuration optimale"
            elif current_price > ma_20 > ma_50:
                ma_score = 4
                ma_signal = "🟡 TENDANCE HAUSSIÈRE - Signaux positifs"
            elif ma_20 > ma_50:
                ma_score = 3
                ma_signal = "⚪ TENDANCE NEUTRE POSITIVE - Attente de confirmation"
            elif current_price > ma_50:
                ma_score = 2
                ma_signal = "🟠 TENDANCE INCERTAINE - Risques émergents"
            else:
                ma_score = 1
                ma_signal = "🔴 TENDANCE BAISSIÈRE - Configuration défavorable"
            
            scores['moving_averages'] = ma_score
            signals['moving_averages'] = ma_signal
            detailed_metrics.update({
                'ma_20': round(ma_20, 2),
                'ma_50': round(ma_50, 2),
                'ma_200': round(ma_200, 2),
                'price_vs_ma20': round(((current_price - ma_20) / ma_20) * 100, 1),
                'golden_cross': ma_20 > ma_50
            })
            
            # 3. MACD计算
            exp12 = hist_data['Close'].ewm(span=12, adjust=False).mean()
            exp26 = hist_data['Close'].ewm(span=26, adjust=False).mean()
            macd_line = exp12 - exp26
            macd_signal = macd_line.ewm(span=9, adjust=False).mean()
            macd_histogram = macd_line - macd_signal
            
            current_macd = macd_line.iloc[-1]
            current_signal = macd_signal.iloc[-1]
            current_histogram = macd_histogram.iloc[-1]
            
            # MACD评分和信号
            if current_macd > current_signal and current_histogram > 0 and current_macd > 0:
                macd_score = 5
                macd_signal = "🟢 FORT SIGNAL HAUSSIER - Momentum accélérant"
            elif current_macd > current_signal:
                macd_score = 4
                macd_signal = "🟡 SIGNAL HAUSSIER - Croisement positif confirmé"
            elif abs(current_macd - current_signal) < 0.001:
                macd_score = 3
                macd_signal = "⚪ TRANSITION - Point d'inflexion potentiel"
            elif current_macd < current_signal and current_macd > 0:
                macd_score = 2
                macd_signal = "🟠 SIGNAL BAISSIER - Momentum décélérant"
            else:
                macd_score = 1
                macd_signal = "🔴 FORT SIGNAL BAISSIER - Momentum négatif fort"
            
            scores['macd'] = macd_score
            signals['macd'] = macd_signal
            detailed_metrics.update({
                'macd_line': round(current_macd, 4),
                'macd_signal': round(current_signal, 4),
                'macd_histogram': round(current_histogram, 4)
            })
            
            # 4. 布林带计算
            bb_middle = hist_data['Close'].rolling(window=20).mean()
            bb_std = hist_data['Close'].rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            current_bb_upper = bb_upper.iloc[-1]
            current_bb_lower = bb_lower.iloc[-1]
            current_bb_middle = bb_middle.iloc[-1]
            
            bb_position = (current_price - current_bb_lower) / (current_bb_upper - current_bb_lower)
            bb_width = (current_bb_upper - current_bb_lower) / current_bb_middle * 100
            
            # 布林带评分和信号
            if bb_position < 0.1:
                bb_score = 5
                bb_signal = "🟢 FORT SURVENDU - Rebond probable"
            elif bb_position < 0.3:
                bb_score = 4
                bb_signal = "🟡 SURVENDU MODÉRÉ - Opportunité intéressante"
            elif bb_position < 0.7:
                bb_score = 3
                bb_signal = "⚪ ZONE NEUTRE - Équilibre acheteurs/vendeurs"
            elif bb_position < 0.9:
                bb_score = 2
                bb_signal = "🟠 SURACHETÉ MODÉRÉ - Prudence nécessaire"
            else:
                bb_score = 1
                bb_signal = "🔴 FORT SURACHETÉ - Correction probable"
            
            # 波动性分析
            if bb_width < 8:
                bb_signal += " | 📏 FAIBLE VOLATILITÉ (Compression - mouvement imminent)"
            elif bb_width > 20:
                bb_signal += " | 🌊 FORTE VOLATILITÉ (Expansion - mouvement en cours)"
            else:
                bb_signal += " | 📊 VOLATILITÉ NORMALE"
            
            scores['bollinger_bands'] = bb_score
            signals['bollinger_bands'] = bb_signal
            detailed_metrics.update({
                'bb_position': round(bb_position, 3),
                'bb_width': round(bb_width, 1),
                'bb_upper': round(current_bb_upper, 2),
                'bb_lower': round(current_bb_lower, 2),
                'bb_middle': round(current_bb_middle, 2)
            })
            
            # 5. 动量计算
            price_1m_ago = hist_data['Close'].iloc[-22] if len(hist_data) > 22 else hist_data['Close'].iloc[0]
            price_change = ((current_price - price_1m_ago) / price_1m_ago) * 100
            
            if price_change >= 15:
                momentum_score = 5
                momentum_signal = "🟢 FORT MOMENTUM HAUSSIER - Accélération"
            elif price_change >= 8:
                momentum_score = 4
                momentum_signal = "🟡 BON MOMENTUM HAUSSIER - Croissance soutenue"
            elif price_change >= -5:
                momentum_score = 3
                momentum_signal = "⚪ MOMENTUM NEUTRE - Stabilité"
            elif price_change >= -8:
                momentum_score = 2
                momentum_signal = "🟠 MOMENTUM BAISSIER - Légère pression"
            else:
                momentum_score = 1
                momentum_signal = "🔴 FORT MOMENTUM BAISSIER - Correction"
            
            scores['momentum'] = momentum_score
            signals['momentum'] = momentum_signal
            detailed_metrics['price_change_1m'] = round(price_change, 1)
            
            # 计算技术分析总分
            technical_score = sum(scores.values()) / len(scores)
            
            detailed_metrics['current_price'] = round(current_price, 2)
            
            return {
                'total_score': round(technical_score, 2),
                'detailed_scores': scores,
                'metrics': detailed_metrics,
                'signals': signals
            }
            
        except Exception as e:
            print(f"Erreur calcul technique: {e}")
            return {'total_score': 0, 'detailed_scores': {}, 'metrics': {}, 'signals': {}}

    def calculate_fundamental_analysis(self, info):
        """计算完整的基本面分析 - 修复版本"""
        scores = {}
        signals = {}
        detailed_metrics = {}
        
        try:
            # 1. PER分析 - 保持不变，这个相对准确
            pe_ratio = info.get('trailingPE', 0) or info.get('forwardPE', 0) or 0
            if pe_ratio <= 15:
                pe_score = 5
                pe_signal = "🟢 SOUS-ÉVALUÉ - Valorisation attractive"
            elif pe_ratio <= 20:
                pe_score = 4
                pe_signal = "🟡 VALORISATION RAISONNABLE - Prix correct"
            elif pe_ratio <= 25:
                pe_score = 3
                pe_signal = "⚪ VALORISATION NEUTRE - Dans la moyenne"
            elif pe_ratio <= 30:
                pe_score = 2
                pe_signal = "🟠 SURÉVALUÉ MODÉRÉ - Prudence"
            else:
                pe_score = 1
                pe_signal = "🔴 FORT SURÉVALUÉ - Risque de correction"
            
            scores['pe_ratio'] = pe_score
            signals['pe_ratio'] = pe_signal
            detailed_metrics['pe_ratio'] = round(pe_ratio, 1)
            
            # 2. 股息率分析 - 修复版本
            dividend_yield = info.get('dividendYield', 0) or 0
            dividend_yield_percent = dividend_yield 
            
            # 添加数据验证和限制
            if dividend_yield_percent > 20:  # 如果超过20%，很可能是数据错误
                st.warning(f"⚠️ Rendement de dividende anormal détecté: {dividend_yield_percent}%")
                dividend_yield_percent = min(dividend_yield_percent, 10)  # 限制到合理范围
            
            dividend_rate = info.get('dividendRate', 0)
            
            # 修正评分标准
            if dividend_yield_percent >= 5.0:
                dividend_score = 5
                dividend_signal = "🟢 RENDEMENT ÉLEVÉ - Très attractif"
            elif dividend_yield_percent >= 3.0:
                dividend_score = 4
                dividend_signal = "🟡 BON RENDEMENT - Intéressant"
            elif dividend_yield_percent >= 1.5:
                dividend_score = 3
                dividend_signal = "⚪ RENDEMENT MODESTE - Correct"
            elif dividend_yield_percent >= 0.5:
                dividend_score = 2
                dividend_signal = "🟠 FAIBLE RENDEMENT - Peu attractif"
            else:
                dividend_score = 1
                dividend_signal = "🔴 RENDEMENT NÉGLIGEABLE - Pour la croissance"
            
            scores['dividend_yield'] = dividend_score
            signals['dividend_yield'] = dividend_signal
            detailed_metrics.update({
                'dividend_yield': round(dividend_yield_percent, 2),
                'dividend_rate': round(dividend_rate, 2) if dividend_rate else 0
            })
            
            # 3. ROE分析 - 保持不变
            roe = info.get('returnOnEquity', 0) or 0
            roe_percent = roe * 100
            
            if roe_percent >= 20:
                roe_score = 5
                roe_signal = "🟢 EXCELLENTE RENTABILITÉ - Management efficace"
            elif roe_percent >= 15:
                roe_score = 4
                roe_signal = "🟡 BONNE RENTABILITÉ - Performance solide"
            elif roe_percent >= 10:
                roe_score = 3
                roe_signal = "⚪ RENTABILITÉ MOYENNE - Dans les normes"
            elif roe_percent >= 5:
                roe_score = 2
                roe_signal = "🟠 FAIBLE RENTABILITÉ - Amélioration nécessaire"
            else:
                roe_score = 1
                roe_signal = "🔴 RENTABILITÉ INSUFFISANTE - Problème structurel"
            
            scores['roe'] = roe_score
            signals['roe'] = roe_signal
            detailed_metrics['roe'] = round(roe_percent, 1)
            
            # 4. 营收增长分析 - 保持不变
            revenue_growth = info.get('revenueGrowth', 0) or 0
            revenue_growth_percent = revenue_growth * 100
            total_revenue = info.get('totalRevenue', 0)
            
            if revenue_growth_percent >= 15:
                growth_score = 5
                growth_signal = "🟢 FORTE CROISSANCE - Expansion rapide"
            elif revenue_growth_percent >= 8:
                growth_score = 4
                growth_signal = "🟡 BONNE CROISSANCE - Développement sain"
            elif revenue_growth_percent >= 0:
                growth_score = 3
                growth_signal = "⚪ CROISSANCE MODESTE - Stabilité"
            elif revenue_growth_percent >= -5:
                growth_score = 2
                growth_signal = "🟠 DÉCLIN MODÉRÉ - Difficultés temporaires"
            else:
                growth_score = 1
                growth_signal = "🔴 FORTE RÉGRESSION - Problèmes structurels"
            
            scores['revenue_growth'] = growth_score
            signals['revenue_growth'] = growth_signal
            detailed_metrics.update({
                'revenue_growth': round(revenue_growth_percent, 1),
                'total_revenue': total_revenue
            })
            
            # 5. 负债率分析 - 修复版本
            debt_to_equity = info.get('debtToEquity', 0) or 0
            total_debt = info.get('totalDebt', 0)
            
            # 修正分类逻辑
            if debt_to_equity <= 0.5:
                debt_score = 5
                debt_signal = "🟢 FAIBLE ENDETTEMENT - Structure saine"
            elif debt_to_equity <= 1.0:
                debt_score = 4
                debt_signal = "🟡 ENDETTEMENT MODÉRÉ - Gestion prudente"
            elif debt_to_equity <= 2.0:
                debt_score = 3
                debt_signal = "⚪ ENDETTEMENT MOYEN - Dans les normes"
            elif debt_to_equity <= 3.0:
                debt_score = 2
                debt_signal = "🟠 ENDETTEMENT ÉLEVÉ - Surveillance requise"
            else:
                debt_score = 1
                debt_signal = "🔴 FORT ENDETTEMENT - Risque financier"
            
            scores['debt_to_equity'] = debt_score
            signals['debt_to_equity'] = debt_signal
            detailed_metrics.update({
                'debt_to_equity': round(debt_to_equity, 2),
                'total_debt': total_debt
            })
            
            # 计算基本面总分
            fundamental_score = sum(scores.values()) / len(scores)
            
            return {
                'total_score': round(fundamental_score, 2),
                'detailed_scores': scores,
                'metrics': detailed_metrics,
                'signals': signals
            }
            
        except Exception as e:
            print(f"Erreur analyse fondamentale: {e}")
            return {'total_score': 0, 'detailed_scores': {}, 'metrics': {}, 'signals': {}}

    def get_recommendation(self, fundamental_score, technical_score):
        """生成投资建议"""
        # 权重: 基本面60%, 技术面40%
        total_score = (fundamental_score * 0.6) + (technical_score * 0.4)
        
        if total_score >= 4.0:
            return "🟢 ACHAT", "Opportunité d'investissement exceptionnelle - Facteurs fondamentaux solides et signaux techniques favorables"
        elif total_score >= 3.5:
            return "🟢 ACHAT", "Bonne opportunité d'investissement - Profil risque/rendement attractif"
        elif total_score >= 3.0:
            return "🟡 NE RIEN FAIRE", "Situation de marché neutre - Attendre des signaux plus convaincants"
        elif total_score >= 2.5:
            return "🟠 SURVEILLER", "Potentiel de retournement - Surveiller les prochaines publications"
        elif total_score >= 2.0:
            return "🔴 VENTE", "Risque de correction - Facteurs défavorables dominants"
        else:
            return "🔴 VENTE", "Forte recommandation de vente - Risques importants identifiés"

    def run_analysis(self, company_name):
        """运行公司分析"""
        if company_name not in self.companies:
            return {"error": "Entreprise non trouvée"}
        
        ticker = self.companies[company_name]["ticker"]
        
        data = self.get_stock_data(ticker)
        if not data['success']:
            return {"error": f"Erreur de données: {data.get('error', 'Unknown')}"}
        
        # 计算得分
        fundamental_result = self.calculate_fundamental_analysis(data['info'])
        technical_result = self.calculate_technical_indicators(data['hist'])
        
        # 生成推荐
        recommendation, justification = self.get_recommendation(
            fundamental_result['total_score'],
            technical_result['total_score']
        )
        
        total_score = round(
            (fundamental_result['total_score'] * 0.6) + 
            (technical_result['total_score'] * 0.4), 2
        )
        
        result = {
            'company_name': company_name,
            'ticker': ticker,
            'team_member': self.team_members[company_name],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'description': self.companies[company_name]["description"],
            'color': self.companies[company_name]["color"],
            'current_price': technical_result['metrics'].get('current_price', 0),
            'fundamental_score': fundamental_result['total_score'],
            'technical_score': technical_result['total_score'],
            'total_score': total_score,
            'recommendation': recommendation,
            'justification': justification,
            'metrics': {
                **fundamental_result['metrics'],
                **technical_result['metrics']
            },
            'detailed_scores': {
                'fundamental': fundamental_result['detailed_scores'],
                'technical': technical_result['detailed_scores']
            },
            'fundamental_signals': fundamental_result['signals'],
            'technical_signals': technical_result['signals'],
            'hist_data': data['hist']
        }
        
        return result