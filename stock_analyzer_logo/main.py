# main.py 完整代码

"""  
主程序入口  
"""  

import streamlit as st  
import base64

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
        
        # 主界面 - Logo在右侧
        col1, col2 = st.columns([8, 2])
        with col1:
            st.title("📊 ESIG.TRADING")  
        with col2:
            # 使用Base64编码的SVG
            logo_svg = """
            <svg xmlns="http://www.w3.org/2000/svg" width="120" height="30" viewBox="0 0 331 76">
                <path fill="#e11418" d="M289.651 13.1v6.105h-.602v.086s.172 0 .43.086c.344.172.86.516.946 1.634-.172-.172 4.128.172 4.128.172l2.064 39.389h16.34l.516-48.763s2.752-1.204 16.77.344c.086-.086-17.544-6.45-40.592.946z"/>
                <path fill="#004380" d="M57.535 31.847l-1.634.086s-.258-9.116-7.999-9.116c-4.73 0-7.482 2.838-7.482 6.364.086 5.418 5.848 6.794 9.289 7.482 4.472.86 11.782 1.806 11.18 11.352-.516 8.17-5.848 11.61-11.267 12.127-3.612.344-7.396-.258-11.18-.43-.688 0-1.978.258-1.978.258V47.24h1.806c.086 0 .602 11.61 9.546 11.009 5.677-.43 7.913-4.042 8.085-7.569.172-4.3-1.978-6.966-8.085-8.084-6.45-1.204-11.352-3.612-11.438-10.578-.086-7.826 6.45-11.008 10.75-11.008 4.387 0 6.02.86 7.483.946 1.204.172 2.838.086 2.838.086zm52.546 0s-1.548-9.718-11.868-9.374c-9.89.516-12.04 9.374-12.04 18.662.086 10.578 4.128 17.803 12.642 17.459 4.73-.172 6.966-1.634 6.88-1.634V45.78h-5.16v-1.893h17.372v1.892h-5.504l-.086 13.76h-4.472c-3.268 0-6.02.259-11.008.689-10.32.86-17.63-4.558-17.544-18.92.086-12.385 5.504-20.555 17.974-20.125 2.924.086 6.02.344 8.6.516 3.182.258 5.504.258 5.504.258v9.89h-1.29zm138.204-.086zm0 0c-.002-.011-1.554-9.804-11.868-9.374-9.89.516-12.04 9.374-12.04 18.662.085 10.579 4.127 17.115 12.727 17.287 9.289.172 11.095-9.375 11.095-9.375h1.462v10.493h-3.612c-3.268 0-6.02.516-11.009.688-8.686.258-17.458-4.558-17.372-18.92.086-12.385 6.794-20.555 17.802-20.125 2.925.086 6.02.344 8.6.516 3.183.258 5.505.258 5.505.258v9.89zm-86.26 26.403h12.385c6.106 0 6.45-10.32 6.45-10.32h1.548v11.954h-31.476v-1.634h4.816v-34.83h-4.816v-1.635h16.254v1.634h-5.16zm51.171-36.55v9.631h-1.462c.086 0 0-7.912-5.16-7.912H195.48v15.05h5.332c2.752 0 4.214-2.752 4.214-5.246v-1.29h1.548v14.878h-1.548v-1.892c0-2.494-1.806-4.73-4.3-4.73h-5.246v17.803h12.47c5.848 0 6.536-10.32 6.536-10.32h1.462v12.04h-31.304v-1.72h4.816V23.333h-4.816V21.7zm-68.543 0v9.631h-1.462c.086 0 0-7.912-5.16-7.912h-11.094v15.05h5.332c2.752 0 4.214-2.752 4.214-5.246v-1.29h1.548v14.878h-1.548v-1.892c0-2.494-1.806-4.73-4.3-4.73h-5.246v17.803h12.47c5.849 0 6.537-10.32 6.537-10.32h1.462v12.04H116.1v-1.72h4.816V23.333H116.1V21.7zm-77.228 1.891h-4.988v-1.72h16.34v1.72h-5.16v34.573h5.16v1.634h-16.34v-1.634h4.988zm-38.873-1.892v9.632H27.09c.086 0 0-7.912-5.16-7.912H10.836v15.05h5.332c2.752 0 4.214-2.752 4.214-5.246v-1.29h1.548v14.878h-1.548v-1.892c0-2.494-1.806-4.73-4.3-4.73h-5.246v17.803h12.47c5.848 0 6.536-10.32 6.536-10.32h1.462v12.04H0v-1.72h4.816V23.333H0V21.7z"/>
                <path fill="#e11418" d="M289.05 6.649c0 .172-16.427-7.482-41.453-2.408 0 0 17.114-7.31 41.366-.774"/>
                <path fill="#e11418" d="M288.963 6.649c0 .172 16.426-7.482 41.452-2.408 0 0-17.114-7.31-41.366-.774m-.688 15.653v-6.107c-23.22-7.396-40.85-1.032-40.85-1.032 14.104-1.634 16.856-.344 16.856-.344l.516 48.763h16.426l2.15-39.389s4.3-.344 4.128-.172c.086-1.032.602-1.462.946-1.634.258-.086.43-.086.43-.086v-.086h-.602z"/>
            </svg>
            """
            
            st.markdown(f"""
            <div style='text-align: right; padding-top: 10px;'>
                {logo_svg}
            </div>
            """, unsafe_allow_html=True)
            
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

