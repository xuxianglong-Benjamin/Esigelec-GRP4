"""
工具函数
"""

import streamlit as st
from datetime import datetime

def setup_page_config():
    """设置页面配置"""
    st.set_page_config(
        page_title="Analyse Multi-Entreprises Complète",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def create_sidebar(companies, team_members):
    """创建侧边栏"""
    st.sidebar.title("🏢 Sélection d'Entreprise")
    
    # 团队信息
    st.sidebar.markdown("### 👥 Équipe d'Analyse")
    for company, member in team_members.items():
        st.sidebar.write(f"**{company}**: {member}")
    
    st.sidebar.markdown("---")
    
    # 公司选择
    selected_company = st.sidebar.selectbox(
        "Choisissez une entreprise:",
        list(companies.keys()),
        index=2
    )
    
    analyze_btn = st.sidebar.button("🚀 Lancer l'Analyse", type="primary")
    
    return selected_company, analyze_btn

def format_currency(value):
    """格式化货币显示"""
    if value >= 1e9:
        return f"€{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"€{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"€{value/1e3:.2f}K"
    else:
        return f"€{value:.2f}"

def validate_data(data):
    """验证数据完整性"""
    if not data or 'success' not in data or not data['success']:
        return False, "数据获取失败"
    
    if 'info' not in data or not data['info']:
        return False, "公司信息缺失"
    
    if 'hist' not in data or data['hist'].empty:
        return False, "历史价格数据缺失"
    
    return True, "数据验证通过"

def get_color_for_score(score):
    """根据分数返回颜色"""
    if score >= 4.0:
        return "green"
    elif score >= 3.0:
        return "orange"
    elif score >= 2.0:
        return "yellow"
    else:
        return "red"

def format_percentage(value):
    """格式化百分比显示"""
    return f"{value:.2f}%"

def format_number(value):
    """格式化数字显示"""
    if isinstance(value, (int, float)):
        if value == 0:
            return "0"
        elif abs(value) < 0.01:
            return f"{value:.6f}"
        elif abs(value) < 0.1:
            return f"{value:.4f}"
        elif abs(value) < 1:
            return f"{value:.3f}"
        elif abs(value) < 10:
            return f"{value:.2f}"
        elif abs(value) < 100:
            return f"{value:.1f}"
        else:
            return f"{value:.0f}"
    return str(value)