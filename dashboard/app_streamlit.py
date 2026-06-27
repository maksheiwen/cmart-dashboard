"""
DASHBOARD: Social Network-Based Loyalty Influencer Program for Shopping Malls
Case Study: Cmart Changlun

v2.0 - Enhanced with "Wow Factor" features:
- Interactive Plotly charts
- Download buttons
- Dark mode toggle
- Animated metrics
- Topic explorer
- SNA network with node info
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
import base64
import re
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Cmart Changlun Analytics Dashboard",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR WOW FACTOR (ENHANCED)
# ============================================================================

st.markdown("""
<style>
    /* ===== Animated gradient header ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* ===== Light mode (default) ===== */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
        color: #000000;
    }
    
    /* ===== Enhanced Metric Cards ===== */
    .stMetric {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 0.8rem 1.2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 0.5rem;
    }
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
    }
    
    /* ===== Sidebar styling ===== */
    .css-1d391kg, .stSidebar {
        background: linear-gradient(180deg, #ffffff 0%, #f0f4fa 100%) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* ===== Gradient dividers ===== */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #667eea, transparent) !important;
        margin: 1.5rem 0 !important;
        opacity: 0.4;
    }
    
    /* ===== Enhanced Tab styling ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid transparent;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.08);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* ===== Topic pills with gradient ===== */
    span[style*="background:#667eea"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 4px 14px !important;
        border-radius: 20px !important;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    /* ===== Dataframe styling ===== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    
    /* ===== Info box styling ===== */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea !important;
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    
    /* ===== Dark mode toggle (your existing toggle) ===== */
    .stApp.dark-mode {
        background: #1a1a2e !important;
        color: #e0e0e0 !important;
    }
    
    .stApp.dark-mode .stMetric {
        background: rgba(30, 30, 60, 0.85) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    
    .stApp.dark-mode .stMetric label {
        color: #a0a0c0 !important;
    }
    
    .stApp.dark-mode .stMetric value {
        color: #667eea !important;
    }
    
    .stApp.dark-mode .stMarkdown,
    .stApp.dark-mode .stCaption,
    .stApp.dark-mode .stHeading {
        color: #e0e0e0 !important;
    }
    
    .stApp.dark-mode .stAlert {
        background: rgba(30, 30, 60, 0.8) !important;
        color: #d0d0d0 !important;
    }
    
    .stApp.dark-mode .stDataFrame {
        background: #1a1a2e !important;
    }
    
    /* ===== Prevent phone system dark mode from overriding ===== */
    @media (prefers-color-scheme: dark) {
        .stApp:not(.dark-mode) {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%) !important;
            color: #000000 !important;
        }
        .stApp:not(.dark-mode) .stMetric label {
            color: #000000 !important;
        }
        .stApp:not(.dark-mode) .stMetric value {
            color: #667eea !important;
        }
        .stApp:not(.dark-mode) .stMarkdown,
        .stApp:not(.dark-mode) .stCaption,
        .stApp:not(.dark-mode) .stHeading {
            color: #000000 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_sentiment_data(name):
    """Load sentiment results CSV for vendor or customer"""
    path = f"outputs/{name}/sentiment_results.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        counts = df['sentiment'].value_counts()
        return df, counts
    return None, None

def load_topic_data(name):
    """Load topics CSV for vendor or customer"""
    path = f"outputs/{name}/topics.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def load_comparison_data():
    """Generate comparison data from vendor and customer CSVs"""
    vendor_df, _ = load_sentiment_data('vendor')
    customer_df, _ = load_sentiment_data('customer')
    
    if vendor_df is not None and customer_df is not None:
        vendor_counts = vendor_df['sentiment'].value_counts()
        customer_counts = customer_df['sentiment'].value_counts()
        
        comparison = pd.DataFrame({
            'Sentiment': ['positive', 'neutral', 'negative'],
            'Vendor': [
                vendor_counts.get('positive', 0),
                vendor_counts.get('neutral', 0),
                vendor_counts.get('negative', 0)
            ],
            'Customer': [
                customer_counts.get('positive', 0),
                customer_counts.get('neutral', 0),
                customer_counts.get('negative', 0)
            ]
        })
        return comparison
    return None

def get_download_link(df, filename):
    """Generate download link for CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
    return href

def show_wordcloud(name):
    """Display word cloud image with zoom capability"""
    path = f"outputs/{name}/wordcloud_{name}.png"
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width='stretch')
        # Add download button
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f'<a href="data:image/png;base64,{data}" download="wordcloud_{name}.png">📥 Download Word Cloud</a>', unsafe_allow_html=True)
    else:
        st.info(f"Word cloud for {name} not found")

def show_sentiment_pie(name):
    """Display sentiment pie chart using Plotly (interactive)"""
    path = f"outputs/{name}/sentiment_pie.png"
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width='stretch')
    else:
        st.info(f"Sentiment pie chart for {name} not found")

def show_sentiment_pie_plotly(name):
    """Display interactive sentiment pie chart using Plotly"""
    df, _ = load_sentiment_data(name)
    if df is not None:
        counts = df['sentiment'].value_counts().reset_index()
        counts.columns = ['Sentiment', 'Count']
        
        colors = {'positive': '#2ecc71', 'neutral': '#f1c40f', 'negative': '#e74c3c'}
        fig = px.pie(
            counts, 
            values='Count', 
            names='Sentiment',
            color='Sentiment',
            color_discrete_map=colors,
            title=f'{name.capitalize()} Sentiment Distribution',
            hole=0.4,
            hover_data=['Count']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            font=dict(size=14),
            margin=dict(l=20, r=20, t=50, b=20),
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info(f"Sentiment data for {name} not found")

def show_class_wordcloud(name, sentiment_class):
    """Display class-specific word cloud"""
    path = f"outputs/{name}/wordcloud_{sentiment_class}.png"
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width='stretch')
    else:
        st.info(f"Word cloud for {name} - {sentiment_class} not found")

def show_topics(name):
    """Display topics as expandable cards with word cloud preview"""
    topics = load_topic_data(name)
    if topics is not None:
        for i, row in topics.iterrows():
            with st.expander(f"📌 Topic {row['topic_id']} - Click to expand"):
                # Show keywords as pills
                keywords = row['keywords'].split()
                pill_html = " ".join([f'<span style="background:#667eea;color:white;padding:4px 12px;border-radius:20px;margin:2px;display:inline-block;font-size:14px;">{kw}</span>' for kw in keywords[:8]])
                st.markdown(pill_html, unsafe_allow_html=True)
                
                # Show topic word cloud preview
                wc_path = f"outputs/{name}/topic_wordcloud_{row['topic_id']}.png"
                if os.path.exists(wc_path):
                    img = Image.open(wc_path)
                    st.image(img, width='stretch')
    else:
        st.info(f"Topics for {name} not found")

def show_topics_barchart(name):
    """Display topic bar chart"""
    path = f"outputs/{name}/topics_barchart.png"
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width='stretch')
    else:
        st.info(f"Topic barchart for {name} not found")

def show_topic_wordcloud(name, topic_id):
    """Display topic word cloud"""
    path = f"outputs/{name}/topic_wordcloud_{topic_id}.png"
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width='stretch')
    else:
        st.info(f"Topic word cloud for {name} Topic {topic_id} not found")

def show_sna_network(zoom_factor=1.0):
    """Display SNA network (Sigma.js if available, else SVG)"""
    # Check for Sigma.js interactive version
    if os.path.exists("outputs/sna/network/index.html"):
        st.components.v1.html(
            open("outputs/sna/network/index.html", 'r', encoding='utf-8').read(),
            height=700
        )
        return
    
    # Check for SVG version
    svg_path = "outputs/sna/network.svg"
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding='utf-8') as f:
            svg_content = f.read()
        # Remove fixed width/height to let it scale to container
        svg_content = re.sub(r'width="[^"]*"', '', svg_content)
        svg_content = re.sub(r'height="[^"]*"', '', svg_content)
        
        # Get original viewBox, if any
        viewbox_match = re.search(r'viewBox="([^"]*)"', svg_content)
        if viewbox_match:
            viewbox = viewbox_match.group(1)
            # Zoom: multiply the width and height by zoom_factor
            parts = viewbox.split()
            if len(parts) == 4:
                x, y, w, h = map(float, parts)
                # Center the zoom on the center of the viewBox
                center_x = x + w/2
                center_y = y + h/2
                new_w = w / zoom_factor   # larger zoom_factor shrinks the viewBox (zooms in)
                new_h = h / zoom_factor
                new_x = center_x - new_w/2
                new_y = center_y - new_h/2
                new_viewbox = f"{new_x} {new_y} {new_w} {new_h}"
                svg_content = re.sub(r'viewBox="[^"]*"', f'viewBox="{new_viewbox}"', svg_content)
            else:
                # If no proper viewBox, set a default
                svg_content = svg_content.replace('<svg', '<svg viewBox="-500 -500 2000 2000"')
        else:
            # No viewBox at all, set a default
            svg_content = svg_content.replace('<svg', '<svg viewBox="-500 -500 2000 2000"')
        
        # Ensure the SVG scales to fill the container
        svg_content = svg_content.replace('<svg', '<svg style="width:100%;height:100%;"')
        
        st.components.v1.html(
            f"""
            <div style='width:100%;height:600px;overflow:auto;border:1px solid #ddd;border-radius:10px;background:#f8f9fa;padding:10px;display:flex;align-items:center;justify-content:center;'>
                {svg_content}
            </div>
            """,
            height=620
        )
        return
    
    # Neither found
    st.info("SNA network not found. Please ask your teammate to export Gephi as Sigma.js template or SVG.")
    st.markdown("""
    **Guidance for SNA teammate:**
    1. **For Sigma.js (interactive):**
       - Install SigmaExporter plugin in Gephi
       - File → Export → Sigma.js template...
       - Export to `outputs/sna/network/`
    
    2. **For SVG (static):**
       - In Gephi: File → Export → SVG...
       - Save as `outputs/sna/network.svg`
    """)

def show_comparison_chart_plotly():
    """Display interactive comparison bar chart using Plotly"""
    comparison = load_comparison_data()
    if comparison is not None:
        fig = go.Figure(data=[
            go.Bar(name='Vendor', x=comparison['Sentiment'], y=comparison['Vendor'], 
                   marker_color='#3498db', text=comparison['Vendor'], textposition='outside'),
            go.Bar(name='Customer', x=comparison['Sentiment'], y=comparison['Customer'], 
                   marker_color='#2ecc71', text=comparison['Customer'], textposition='outside')
        ])
        fig.update_layout(
            title='Vendor vs Customer Sentiment Comparison',
            xaxis_title='Sentiment',
            yaxis_title='Count',
            barmode='group',
            font=dict(size=14),
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Comparison data not available")

# ============================================================================
# LOAD DATA
# ============================================================================

vendor_sent_df, vendor_sent_counts = load_sentiment_data('vendor')
customer_sent_df, customer_sent_counts = load_sentiment_data('customer')
vendor_topics = load_topic_data('vendor')
customer_topics = load_topic_data('customer')
comparison_df = load_comparison_data()

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/shopping-mall.png", width=80)
    st.title("🏬 Cmart Changlun")
    st.caption("Analytics Dashboard")
    st.divider()
    
    page = st.radio(
        "Navigate",
        ["📊 Overview", 
         "👨‍💼 Vendor Analysis", 
         "👤 Customer Analysis", 
         "🌐 SNA Network",
         "📈 Comparison & Recommendations",
         "ℹ️ About & Methodology"],
        index=0
    )
    
    st.divider()
    st.caption("🔗 Social Network-Based Loyalty Influencer Program")
    st.caption(f"v2.0 | {datetime.now().strftime('%Y-%m-%d')}")
    
    # Dark mode toggle (experimental)
    st.divider()
    dark_mode = st.toggle("🌙 Dark Mode", value=False)
    if dark_mode:
        st.markdown("""
        <style>
            .stApp { background: #1a1a2e; color: #e0e0e0; }
            .stMetric { background: rgba(30, 30, 60, 0.85) !important; border: 1px solid rgba(255,255,255,0.05) !important; box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important; }
            .stMetric label { color: #a0a0c0 !important; }
            .stMetric value { color: #667eea !important; }
            .stMarkdown, .stCaption, .stHeading { color: #e0e0e0 !important; }
            .stAlert { background: rgba(30, 30, 60, 0.8) !important; color: #d0d0d0 !important; }
            .stDataFrame { background: #1a1a2e !important; }
        </style>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE CONTENT
# ============================================================================

# --- OVERVIEW PAGE ---
if page == "📊 Overview":
    st.markdown("""
    <div class="main-header">
        <h1>🏬 Cmart Changlun Analytics Dashboard</h1>
        <p>Social Network-Based Loyalty Influencer Program for Shopping Malls</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if vendor_sent_counts is not None:
            total = vendor_sent_counts.sum()
            pos = vendor_sent_counts.get('positive', 0)
            st.metric(
                label="🛍️ Vendor Sentiment",
                value=f"{pos/total*100:.0f}% Positive",
                help="Sentiment analysis from vendor interview"
            )
        else:
            st.metric(label="🛍️ Vendor Sentiment", value="N/A")
    
    with col2:
        if customer_sent_counts is not None:
            total = customer_sent_counts.sum()
            pos = customer_sent_counts.get('positive', 0)
            st.metric(
                label="👤 Customer Sentiment",
                value=f"{pos/total*100:.0f}% Positive",
                help="Sentiment analysis from customer interviews"
            )
        else:
            st.metric(label="👤 Customer Sentiment", value="N/A")
    
    with col3:
        if vendor_topics is not None:
            n_topics = len(vendor_topics)
            st.metric(
                label="📝 Vendor Topics",
                value=f"{n_topics} Topics",
            )
        else:
            st.metric(label="📝 Vendor Topics", value="N/A")
    
    with col4:
        if customer_topics is not None:
            n_topics = len(customer_topics)
            st.metric(
                label="📝 Customer Topics",
                value=f"{n_topics} Topics",
            )
        else:
            st.metric(label="📝 Customer Topics", value="N/A")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👨‍💼 Vendor Word Cloud")
        show_wordcloud('vendor')
    with col2:
        st.subheader("👤 Customer Word Cloud")
        show_wordcloud('customer')
    
    st.divider()
    
    st.subheader("📈 Sentiment Comparison: Vendor vs Customer")
    show_comparison_chart_plotly()
    
    st.info("💡 **Key Insight:** Customers are generally more positive (31%) than vendors (24%), indicating that shoppers enjoy the Cmart experience, while vendors face operational challenges. However, customers also express more negative feedback (26% vs 10%) regarding parking and pricing. This sentiment gap presents an opportunity for management to address customer pain points while supporting vendor operations. These insights are crucial for designing an effective loyalty program and influencer strategy.")

# --- VENDOR ANALYSIS PAGE ---
elif page == "👨‍💼 Vendor Analysis":
    st.title("👨‍💼 Vendor Analysis")
    st.caption("Analysis from interviews with car boot sales vendors at Cmart Changlun")
    st.divider()
    
    tab1, tab2 = st.tabs(["📊 Sentiment Analysis", "📝 Topic Modeling"])
    
    with tab1:
        st.subheader("📊 Sentiment Distribution")
        show_sentiment_pie_plotly('vendor')
        
        st.divider()
        
        st.subheader("🗂️ Sentiment Word Clouds by Class")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("😊 Positive")
            show_class_wordcloud('vendor', 'positive')
        with col2:
            st.caption("😐 Neutral")
            show_class_wordcloud('vendor', 'neutral')
        with col3:
            st.caption("😞 Negative")
            show_class_wordcloud('vendor', 'negative')
        
        st.divider()
        
        with st.expander("📋 View Full Sentiment Results", expanded=False):
            if vendor_sent_df is not None:
                st.dataframe(vendor_sent_df, width='stretch')
                st.markdown(get_download_link(vendor_sent_df, 'vendor_sentiment.csv'), unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📝 Topics from Vendor Interviews")
        st.caption("Topics identified from vendor conversations about their business at Cmart")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            show_topic_wordcloud('vendor', 1)
            st.caption("Topic 1: Interaction & Social Media")
        with col2:
            show_topic_wordcloud('vendor', 2)
            st.caption("Topic 2: Benefits & Feedback")
        with col3:
            show_topic_wordcloud('vendor', 3)
            st.caption("Topic 3: Products & Situations")
        
        st.divider()
        
        st.subheader("📊 Topic Visualization")
        show_topics_barchart('vendor')

# --- CUSTOMER ANALYSIS PAGE ---
elif page == "👤 Customer Analysis":
    st.title("👤 Customer Analysis")
    st.caption("Analysis from interviews with visitors to Cmart Changlun")
    st.divider()
    
    tab1, tab2 = st.tabs(["📊 Sentiment Analysis", "📝 Topic Modeling"])
    
    with tab1:
        st.subheader("📊 Sentiment Distribution")
        show_sentiment_pie_plotly('customer')
        
        st.divider()
        
        st.subheader("🗂️ Sentiment Word Clouds by Class")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("😊 Positive")
            show_class_wordcloud('customer', 'positive')
        with col2:
            st.caption("😐 Neutral")
            show_class_wordcloud('customer', 'neutral')
        with col3:
            st.caption("😞 Negative")
            show_class_wordcloud('customer', 'negative')
        
        st.divider()
        
        with st.expander("📋 View Full Sentiment Results", expanded=False):
            if customer_sent_df is not None:
                st.dataframe(customer_sent_df, width='stretch')
                st.markdown(get_download_link(customer_sent_df, 'customer_sentiment.csv'), unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📝 Topics from Customer Interviews")
        st.caption("Topics identified from customer conversations about their shopping experience")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            show_topic_wordcloud('customer', 1)
            st.caption("Topic 1: Location & Accessibility")
        with col2:
            show_topic_wordcloud('customer', 2)
            st.caption("Topic 2: Promotions & Recommendations")
        with col3:
            show_topic_wordcloud('customer', 3)
            st.caption("Topic 3: Atmosphere & Community")
        
        st.divider()
        
        st.subheader("📊 Topic Visualization")
        show_topics_barchart('customer')

# --- SNA PAGE ---
elif page == "🌐 SNA Network":
    st.title("🌐 Social Network Analysis")
    st.caption("Social media network analysis from TikTok using hashtags related to Cmart Changlun")
    st.divider()
    
    # --- Summary Metrics (from teammate's analysis) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="👥 Total Nodes",
            value="972",
            help="Unique TikTok users in the network"
        )
    with col2:
        st.metric(
            label="🔗 Total Edges",
            value="73,677",
            help="Shared hashtag pairs between users"
        )
    with col3:
        st.metric(
            label="📊 Network Density",
            value="0.156",
            help="From Gephi statistics"
        )
    with col4:
        st.metric(
            label="🧩 Modularity",
            value="0.256",
            help="Community clusters identified"
        )
    
    st.divider()
    
    # --- Hashtag cards ---
    st.subheader("🏷️ Hashtag Usage Frequency")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#3498db;color:white;padding:10px;border-radius:10px;text-align:center;">
            <strong>#1</strong><br>
            <span style="font-size:18px;">Changlun</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#2ecc71;color:white;padding:10px;border-radius:10px;text-align:center;">
            <strong>#2</strong><br>
            <span style="font-size:18px;">UUM</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#e74c3c;color:white;padding:10px;border-radius:10px;text-align:center;">
            <strong>#3</strong><br>
            <span style="font-size:18px;">ChanglunKedah</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- Interactive Network ---
    st.subheader("🌐 SNA Graph")
    st.caption("High Eigenvector Centrality (Red) · Low Eigenvector Centrality (Blue) · Node size = Degree")
    # Add a zoom slider
    zoom = st.slider(
        "🔍 Zoom Level",
        min_value=1.0,
        max_value=20.0,
        value=5.0,         
        step=0.5
    )
    show_sna_network(zoom_factor=zoom)
    
    st.divider()
    
    # --- Top Influencers Table ---
    st.subheader("🏆 Top 5 Influential Users")
    st.caption("Ranked by Eigenvector Centrality")
    
    influencers_data = {
        "Rank": [1, 2, 3, 4, 5],
        "Username": [
            "Ba'en Changlun",
            "The Daq",
            "Nasi Kerabu Kachi Mall UUM",
            "Ayam Gepuk Sultan Changlun",
            "DET'S PIZZERIA CHANGLUN"
        ],
        "Degree": [3200, 5524, 5152, 3522, 3424],
        "Eigenvector": [0.8313, 0.8099, 0.7946, 0.7439, 0.4174]
    }
    influencers_df = pd.DataFrame(influencers_data)
    st.dataframe(influencers_df, width='stretch', hide_index=True)
    
    st.divider()
    
    # --- Loyalty Program Recommendations ---
    st.subheader("💡 Loyalty Program Recommendations")
    st.caption("Based on SNA Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #667eea, #764ba2);color:white;padding:18px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:32px;">🎯</div>
                <h4 style="margin:10px 0 8px 0;font-size:16px;">Prioritise Top Eigenvector Nodes</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.5;">
                    They reach the widest connected audience.<br>
                    <strong style="opacity:0.8;">Focus on:</strong> Ba'en Changlun, The Daq, Nasi Kerabu Kachi Mall UUM.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.6;">SNA Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #1a1a2e, #16213e);color:white;padding:18px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:32px;">📢</div>
                <h4 style="margin:10px 0 8px 0;font-size:16px;">Re-engage UUM/Kedah Users</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.5;">
                    Bridge campus audience to mall traffic.<br>
                    <strong style="opacity:0.8;">Target:</strong> UUM students and local community.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.6;">Community Engagement</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #00b894, #00a381);color:white;padding:18px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:32px;">📈</div>
                <h4 style="margin:10px 0 8px 0;font-size:16px;">Track Cluster Growth</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.5;">
                    Repeat scraping to monitor influencer reach.<br>
                    <strong style="opacity:0.8;">Measure:</strong> Campaign effectiveness.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.6;">Monitoring</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    st.info("💡 **Insight:** The social network shows an active community discussing Cmart Changlun. Key influencers can be identified to become ambassadors for the loyalty program. This analysis helps identify influential individuals for marketing strategies.")

# --- COMPARISON PAGE ---
elif page == "📈 Comparison & Recommendations":
    st.title("📈 Comparison & Recommendations")
    st.caption("Comparison of Vendor vs Customer findings and recommendations for Cmart management")
    st.divider()
    
    # Sentiment Comparison
    st.subheader("📊 Sentiment Comparison")
    show_comparison_chart_plotly()
    
    st.divider()
    
    # Gap Analysis (Dynamic)
    st.subheader("🔍 Sentiment Gap Analysis")
    
    if vendor_sent_counts is not None and customer_sent_counts is not None:
        v_total = vendor_sent_counts.sum()
        v_pos = vendor_sent_counts.get('positive', 0)
        v_pos_pct = (v_pos / v_total * 100) if v_total > 0 else 0
        
        c_total = customer_sent_counts.sum()
        c_pos = customer_sent_counts.get('positive', 0)
        c_pos_pct = (c_pos / c_total * 100) if c_total > 0 else 0
        
        gap = c_pos_pct - v_pos_pct
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vendor Positive", f"{v_pos_pct:.0f}%")
        with col2:
            st.metric("Customer Positive", f"{c_pos_pct:.0f}%", delta=f"+{gap:.0f}%" if gap > 0 else f"{gap:.0f}%", delta_color="normal" if gap > 0 else "inverse")
        with col3:
            st.metric("Sentiment Gap", f"{gap:.0f}%", delta="Customers more positive" if gap > 0 else "Vendors more positive", delta_color="off")
        
        st.caption(f"Customers are {gap:.0f}% more positive than vendors, indicating a positive shopper experience despite operational challenges.")
    else:
        st.info("Run analysis first to see sentiment gap data.")
    
    st.divider()
    
    # Model Comparison
    st.subheader("⚖️ Model Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧠 Sentiment Models
        
        | Model | F1-Score | Status |
        |-------|----------|--------|
        | **HuggingFace (T5)** | 0.673 | ✅ **Best** |
        | **Multinomial** | 0.650 | ⚠️ Official benchmark |
        
        **Why HuggingFace?** Handles mixed Malay-English text better than the traditional Multinomial model. Transformer-based models capture context more effectively.
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Topic Models
        
        | Model | Coherence | Status |
        |-------|-----------|--------|
        | **LDA** | 0.021 | ✅ **Best** |
        | **NMF** | 0.014 | ⚠️ Less coherent |
        
        **Why LDA?** LDA produces more distinct, interpretable topics with higher coherence scores. The topics are clearer and more actionable.
        """)
    
    st.info("💡 **Why This Matters:** We compared multiple models to ensure the most accurate insights. The selected models (HuggingFace for sentiment, LDA for topics) provide the most reliable analysis for the Cmart context.")
    
    st.divider()
    
    # Topics Side-by-Side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👨‍💼 Vendor Topics")
        if vendor_topics is not None:
            st.dataframe(vendor_topics, width='stretch')
        else:
            st.info("Vendor topics not found")
    with col2:
        st.subheader("👤 Customer Topics")
        if customer_topics is not None:
            st.dataframe(customer_topics, width='stretch')
        else:
            st.info("Customer topics not found")
    
    st.divider()
    
    # --- Key Findings (Insight Cards) ---
    st.subheader("📋 Key Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #f0f4ff, #e8edf5);padding:20px;border-radius:12px;border-left:5px solid #3498db;height:100%;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <span style="font-size:28px;">👨‍💼</span>
                <h3 style="margin:0;color:#2c3e50;font-size:18px;">Vendor Perspective</h3>
            </div>
            <ul style="list-style:none;padding:0;margin:0;font-size:14px;line-height:1.8;color:#34495e;">
                <li><strong style="color:#2980b9;">🍽️ Menu & Products:</strong> Sell milo, laksa, bihun soup</li>
                <li><strong style="color:#2980b9;">📊 Situation:</strong> Depends on crowd &amp; weather</li>
                <li><strong style="color:#2980b9;">🎯 Strategy:</strong> Adapt menu based on demographics</li>
                <li><strong style="color:#2980b9;">📢 Promotion:</strong> Use Facebook &amp; social media</li>
                <li><strong style="color:#2980b9;">⚠️ Challenges:</strong> Competition &amp; uncertain situations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #f0faf4, #e6f2ed);padding:20px;border-radius:12px;border-left:5px solid #2ecc71;height:100%;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <span style="font-size:28px;">👤</span>
                <h3 style="margin:0;color:#2c3e50;font-size:18px;">Customer Perspective</h3>
            </div>
            <ul style="list-style:none;padding:0;margin:0;font-size:14px;line-height:1.8;color:#34495e;">
                <li><strong style="color:#27ae60;">📍 Location:</strong> Easy to access, parking is difficult</li>
                <li><strong style="color:#27ae60;">💰 Price:</strong> Some say expensive, some say affordable</li>
                <li><strong style="color:#27ae60;">🛍️ Products:</strong> Interesting, good variety</li>
                <li><strong style="color:#27ae60;">🧹 Cleanliness:</strong> OK, but some areas still dirty</li>
                <li><strong style="color:#27ae60;">📣 Promotion:</strong> Need more activities</li>
                <li><strong style="color:#27ae60;">😊 Satisfaction:</strong> Will come again, will recommend</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Summary Insights
    st.subheader("💡 Summary Insights from Comparison")
    
    st.markdown("""
    | Aspect | Finding | Implication |
    |--------|---------|-------------|
    | **Sentiment Gap** | Customers more positive (31% vs 24%) | Cmart delivers a good experience; leverage this in marketing |
    | **Negative Gap** | Customers more negative (26% vs 10%) | Address parking, pricing concerns |
    | **Neutral Gap** | Vendors more neutral (66% vs 43%) | Vendors need engagement/support |
    | **Topic Gap** | Vendors focus on operations; customers focus on experience | Align operations with customer expectations |
    | **Model Choice** | HuggingFace + LDA selected | Most accurate models for this context |
    """)
    
    st.divider()
    
    # --- Recommendations (Action Cards) ---
    st.subheader("💡 Recommendations for Cmart Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #3498db, #2980b9);color:white;padding:15px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:28px;">📢</div>
                <h4 style="margin:8px 0 6px 0;font-size:16px;">Enhance Promotions</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.4;">
                    Use SNA influencers for events.<br>
                    More TikTok &amp; Facebook promotions.<br>
                    Weekly/monthly events to attract visitors.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.7;">Action: Marketing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #2ecc71, #27ae60);color:white;padding:15px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:28px;">🏗️</div>
                <h4 style="margin:8px 0 6px 0;font-size:16px;">Improve Infrastructure</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.4;">
                    ✅ Covered paid parking built.<br>
                    Improve area cleanliness.<br>
                    Enhance visitor experience.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.7;">Action: Facilities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #f39c12, #e67e22);color:white;padding:15px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:28px;">🍽️</div>
                <h4 style="margin:8px 0 6px 0;font-size:16px;">Increase Variety</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.4;">
                    Customers want more options.<br>
                    Vendors can add new menu items.<br>
                    Attract diverse audiences.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.7;">Action: Operations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #9b59b6, #8e44ad);color:white;padding:15px;border-radius:12px;height:220px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            <div>
                <div style="font-size:28px;">⭐</div>
                <h4 style="margin:8px 0 6px 0;font-size:16px;">Loyalty Program</h4>
                <p style="font-size:13px;opacity:0.9;margin:0;line-height:1.4;">
                    Points‑based rewards.<br>
                    Discounts for loyal visitors.<br>
                    Influencers to promote program.
                </p>
            </div>
            <div style="font-size:11px;opacity:0.7;">Action: Retention</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.success("✅ **Conclusion:** Cmart Changlun has great potential to become a community destination. With infrastructure improvements (parking) and a more aggressive promotion strategy, an influencer-based loyalty program can further enhance customer satisfaction and vendor business results.")

# --- ABOUT & METHODOLOGY PAGE ---
elif page == "ℹ️ About & Methodology":
    st.title("ℹ️ About & Methodology")
    st.caption("Understanding the Cmart Changlun Analytics Dashboard")
    st.divider()
    
    st.markdown("""
    ### 🎯 Purpose of This Dashboard
    
    This dashboard was developed as part of the **Social Network-Based Loyalty Influencer Program** project for **Cmart Changlun**. It integrates three key data sources to provide actionable insights for mall management:
    
    1. **Vendor Interviews** – Understanding the operational challenges and strategies of vendors at the car boot sales.
    2. **Customer Interviews** – Capturing shopper experiences, pain points, and satisfaction levels.
    3. **Social Media Analysis (SNA)** – Mapping the online community and identifying key influencers discussing Cmart Changlun.
    
    The goal is to design an effective loyalty program leveraging both offline feedback and online influence.
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📊 Methodology Overview
    
    | Component | Method | Details |
    |-----------|--------|---------|
    | **Data Collection** | Interviews | 1 vendor + 3 customers (combined into transcripts) |
    | **Text Preprocessing** | Tokenization, Stopword Removal, Stemming | Using NLTK + Malaya Stopwords |
    | **Sentiment Analysis** | HuggingFace (T5) + Multinomial | Best model selected based on F1-score (0.673) |
    | **Topic Modeling** | LDA vs NMF | LDA selected for better coherence (0.021 vs 0.014) |
    | **SNA** | Gephi + Sigma.js | Network visualization and influencer identification |
    | **Dashboard** | Streamlit | Interactive, downloadable, with dark mode toggle |
    """)
    
    st.divider()
    
    # Dynamic Data Breakdown
    st.subheader("📊 Current Data Breakdown")
    
    vendor_df, vendor_counts = load_sentiment_data('vendor')
    customer_df, customer_counts = load_sentiment_data('customer')
    
    if vendor_counts is not None and customer_counts is not None:
        v_pos = vendor_counts.get('positive', 0)
        v_neu = vendor_counts.get('neutral', 0)
        v_neg = vendor_counts.get('negative', 0)
        v_total = v_pos + v_neu + v_neg
        
        c_pos = customer_counts.get('positive', 0)
        c_neu = customer_counts.get('neutral', 0)
        c_neg = customer_counts.get('negative', 0)
        c_total = c_pos + c_neu + c_neg
        
        st.markdown(f"""
        | Data Source | Interviewees | Sentences Analyzed | Sentiment Breakdown |
        |-------------|--------------|-------------------|---------------------|
        | **Vendor** | 1 vendor | **{v_total} sentences** | {v_pos} Positive, {v_neg} Negative, {v_neu} Neutral |
        | **Customer** | 3 customers | **{c_total} sentences** | {c_pos} Positive, {c_neg} Negative, {c_neu} Neutral |
        | **SNA** | TikTok scrape | 5 hashtags, network nodes/edges | TBD |
        """)
    else:
        st.info("Run analysis first to see dynamic data.")
    
    st.divider()
    
    st.markdown("""
    ### 🧠 How to Use This Dashboard
    
    1. **Navigate** using the sidebar menu.
    2. **Overview** – Get a high-level summary of all findings.
    3. **Vendor/Customer Analysis** – Explore sentiment distributions, word clouds, and topics in detail.
    4. **SNA Network** – View the interactive social media network and identify influencers.
    5. **Comparison & Recommendations** – See how vendor and customer perspectives compare, plus actionable recommendations.
    
    **Bonus Features:**
    - **Dark Mode** – Toggle in the sidebar for low-light viewing.
    - **Download** – Download sentiment results as CSV files.
    - **Interactive Charts** – Hover and zoom on Plotly charts for deeper insights.
    """)
    
    st.divider()
    
    st.markdown("""
    ### 🛠️ Technical Notes
    
    - **Model Selection:** HuggingFace (T5) performed best for mixed Malay-English text. LDA was chosen for topic modeling due to higher coherence scores.
    """)
    
    st.divider()
    
    st.markdown("""
    ### 👥 Team & Acknowledgments
    
    This project was developed by a collaborative team as part of the SULAM program. Special thanks to Cmart Changlun management, vendors, and customers who participated in the interviews.
    """)
    
    st.divider()
    
    st.caption(f"🔄 Dashboard version 2.0 | Last refreshed: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("© 2026 Cmart Changlun Analytics Dashboard")
with col2:
    st.caption("🔗 Social Network-Based Loyalty Influencer Program")
with col3:
    st.caption(f"🔄 Last updated: {datetime.now().strftime('%I:%M %p')}")