"""
主程序入口
"""

import streamlit as st

from analyzer import StockAnalyzer
from visualization import Visualizer
from utils import setup_page_config, create_sidebar
from config import COMPANIES, TEAM_MEMBERS

class Dashboard:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        self.visualizer = Visualizer()
        self.companies = COMPANIES
        self.team_members = TEAM_MEMBERS

    def run(self):
        """运行主仪表盘"""
        setup_page_config()
        
        # 侧边栏
        selected_company, analyze_btn = create_sidebar(self.companies, self.team_members)
        
        # 主界面
        st.title("📊 Analyse Boursière Complète - Projet de Groupe")
        st.markdown("**Système Expert d'Aide à la Décision d'Investissement**")
        st.markdown("---")
        
        # 默认显示或分析结果
        if not analyze_btn and 'last_analysis' not in st.session_state:
            self.visualizer.display_welcome()
        else:
            if analyze_btn or 'last_analysis' in st.session_state:
                company_to_analyze = selected_company
                
                with st.spinner(f"🔍 Analyse en cours pour {company_to_analyze}..."):
                    result = self.analyzer.run_analysis(company_to_analyze)
                
                if 'error' in result:
                    st.error(f"❌ Erreur: {result['error']}")
                else:
                    st.session_state.last_analysis = result
                    self.visualizer.display_analysis_result(result)

def main():
    dashboard = Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main()