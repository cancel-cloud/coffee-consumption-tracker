import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calplot
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, select, func
from datetime import date, datetime, timedelta
import io

# Seiten-Konfiguration - MUST BE FIRST
st.set_page_config(
    page_title="☕ Kaffeekonsum-Tracker",
    layout="wide",
    page_icon="☕"
)

# Initialize session state for quick buttons
if 'quick_buttons' not in st.session_state:
    st.session_state.quick_buttons = []

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #8B4513;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f5dc 0%, #deb887 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #8B4513;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #8B4513;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #deb887;
        padding-bottom: 0.5rem;
    }
    .caffeine-warning {
        background-color: #ffeb3b;
        color: #333;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .caffeine-danger {
        background-color: #f44336;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #d32f2f;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f8ff 0%, #e6e6fa 100%);
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #deb887 !important;
        border-radius: 5px !important;
    }
    .stSelectbox > div > div > div {
        color: #333333 !important;
    }
    .stSelectbox label {
        color: #8B4513 !important;
        font-weight: 600 !important;
    }
    .success-message {
        background-color: #90EE90;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Einführung der Sidebar-Toggles
st.sidebar.markdown("### ⚙️ Einstellungen")
show_varieties = st.sidebar.checkbox("🌱 Sortenverwaltung anzeigen", value=False)
show_quick_settings = st.sidebar.checkbox("⚡ Quick-Entry Einstellungen", value=False)
show_editor = st.sidebar.checkbox("✏️ Einträge bearbeiten & löschen", value=True)
show_stats = st.sidebar.checkbox("📊 Statistiken anzeigen", value=True)
show_pie = st.sidebar.checkbox("🥧 Sorten-Verteilung anzeigen", value=True)
show_heatmap = st.sidebar.checkbox("🗓️ Kalender-Heatmap anzeigen", value=True)
show_caffeine = st.sidebar.checkbox("⚡ Koffein-Tracking anzeigen", value=True)
show_import = st.sidebar.checkbox("📁 Import/Export anzeigen", value=True)

# Datenbank-Setup
engine = create_engine('sqlite:///coffee.db', echo=False)
metadata = MetaData()

consumption = Table(
    'consumption', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date, nullable=False),
    Column('cups', Integer, nullable=False),
    Column('variety_id', Integer, nullable=False),
)
varieties = Table(
    'varieties', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, unique=True, nullable=False),
    Column('caffeine_mg', Integer, default=0),
)
metadata.create_all(engine)

# Check if caffeine_mg column exists, if not add it
try:
    with engine.begin() as conn:
        result = conn.execute("PRAGMA table_info(varieties)")
        columns = [row[1] for row in result]
        if 'caffeine_mg' not in columns:
            conn.execute("ALTER TABLE varieties ADD COLUMN caffeine_mg INTEGER DEFAULT 0")
            st.info("🔄 Datenbank wurde um Koffein-Tracking erweitert!")
except:
    pass

# Sortenverwaltung (optional)
if show_varieties:
    with st.sidebar.expander("🌱 Sorten verwalten", expanded=False):
        df_var = pd.read_sql(select(varieties), engine)
        
        st.markdown("**🆕 Neue Sorte hinzufügen:**")
        col1, col2 = st.columns(2)
        with col1:
            new_var = st.text_input("Sortenname:")
        with col2:
            new_caffeine = st.number_input("Koffein (mg/Tasse):", min_value=0, value=100)
        
        if st.button("➕ Hinzufügen", key='add_var') and new_var:
            with engine.begin() as conn:
                conn.execute(varieties.insert().values(name=new_var, caffeine_mg=new_caffeine))
            st.success(f"✅ Sorte '{new_var}' mit {new_caffeine}mg Koffein hinzugefügt")
            st.rerun()
        
        if not df_var.empty:
            st.markdown("**✏️ Bestehende Sorten bearbeiten:**")
            for _, row in df_var.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.text(row['name'])
                with col2:
                    new_caff = st.number_input(f"Koffein:", value=int(row.get('caffeine_mg', 0)), key=f"caff_{row['id']}")
                with col3:
                    if st.button("💾", key=f"update_{row['id']}"):
                        with engine.begin() as conn:
                            conn.execute(
                                varieties.update()
                                .where(varieties.c.id == row['id'])
                                .values(caffeine_mg=new_caff)
                            )
                        st.success("✅ Aktualisiert!")
                        st.rerun()
        
        if not df_var.empty:
            to_delete = st.multiselect("🗑️ Sorten löschen", df_var['name'])
            if st.button("❌ Löschen", key='del_var') and to_delete:
                with engine.begin() as conn:
                    for name in to_delete:
                        conn.execute(varieties.delete().where(varieties.c.name == name))
                st.success(f"🗑️ Gelöscht: {', '.join(to_delete)}")
                st.rerun()

# Quick Entry Settings (optional)
if show_quick_settings:
    with st.sidebar.expander("⚡ Quick-Entry Buttons konfigurieren", expanded=False):
        df_var = pd.read_sql(select(varieties), engine)
        
        if not df_var.empty:
            st.markdown("**⚡ Wähle Sorten für Quick-Entry Buttons:**")
            
            # Initialize session state for quick buttons if not exists
            if 'quick_buttons' not in st.session_state:
                st.session_state.quick_buttons = []
            
            # Create multiselect for choosing quick button varieties
            selected_varieties = st.multiselect(
                "Sorten für Quick Buttons",
                options=df_var['name'].tolist(),
                default=st.session_state.quick_buttons,
                help="Ausgewählte Sorten erscheinen als Quick-Entry Buttons im Hauptbereich"
            )
            
            # Update session state
            st.session_state.quick_buttons = selected_varieties
            
            if selected_varieties:
                st.success(f"✅ {len(selected_varieties)} Quick Buttons konfiguriert")
                st.markdown("**Konfigurierte Buttons:**")
                for variety in selected_varieties:
                    variety_info = df_var[df_var['name'] == variety].iloc[0]
                    caffeine = int(variety_info.get('caffeine_mg', 0))
                    st.write(f"☕ **{variety}** - {caffeine}mg Koffein/Tasse")
            else:
                st.info("ℹ️ Keine Quick Buttons konfiguriert")
        else:
            st.warning("⚠️ Bitte erst Sorten hinzufügen, um Quick Buttons zu konfigurieren!")

# App-Header
st.markdown('<h1 class="main-header">☕ Kaffeekonsum-Tracker</h1>', unsafe_allow_html=True)

# Daten laden
df = pd.read_sql(
    """
    SELECT c.id, c.date, c.cups, v.name AS variety, v.caffeine_mg,
           (c.cups * v.caffeine_mg) AS total_caffeine
      FROM consumption c
      JOIN varieties v ON c.variety_id = v.id
    """,
    engine, parse_dates=['date']
)

# Quick Stats Header mit Koffein
if not df.empty:
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    total_cups = df['cups'].sum()
    total_caffeine = df['total_caffeine'].sum()
    
    today_data = df[df['date'] == pd.to_datetime(today)]
    today_cups = today_data['cups'].sum()
    today_caffeine = today_data['total_caffeine'].sum()
    
    week_data = df[df['date'] >= pd.to_datetime(week_ago)]
    week_cups = week_data['cups'].sum()
    week_caffeine = week_data['total_caffeine'].sum()
    
    month_data = df[df['date'] >= pd.to_datetime(month_ago)]
    month_cups = month_data['cups'].sum()
    month_caffeine = month_data['total_caffeine'].sum()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("☕ Heute", f"{today_cups} Tassen", delta=None)
    with col2:
        caffeine_color = "normal"
        if today_caffeine > 400:
            caffeine_color = "inverse"
        st.metric("⚡ Koffein heute", f"{today_caffeine}mg", delta=None, delta_color=caffeine_color)
    with col3:
        st.metric("📅 Diese Woche", f"{week_cups} Tassen", delta=None)
    with col4:
        st.metric("⚡ Woche Koffein", f"{week_caffeine}mg", delta=None)
    with col5:
        st.metric("📊 Monat Tassen", f"{month_cups}", delta=None)
    with col6:
        st.metric("🎯 Gesamt Koffein", f"{total_caffeine/1000:.1f}g", delta=None)
    
    # Koffein-Warnung
    if today_caffeine > 400:
        st.markdown(
            '<div class="caffeine-danger">⚠️ <strong>Hoher Koffeinkonsum!</strong> '
            f'Du hast heute {today_caffeine}mg Koffein konsumiert. '
            'Die empfohlene Tageshöchstmenge liegt bei 400mg.</div>',
            unsafe_allow_html=True
        )
    elif today_caffeine > 300:
        st.markdown(
            '<div class="caffeine-warning">⚡ <strong>Achtung:</strong> '
            f'Du hast heute {today_caffeine}mg Koffein konsumiert. '
            'Näherst dich der empfohlenen Tageshöchstmenge von 400mg.</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")

# Neuer Eintrag in schönerer Box
st.markdown('<div class="section-header">➕ Neuen Eintrag hinzufügen</div>', unsafe_allow_html=True)

# Quick Entry Buttons (always visible if configured)
if 'quick_buttons' in st.session_state and st.session_state.quick_buttons:
    df_var = pd.read_sql(select(varieties), engine)
    if not df_var.empty:
        st.markdown("**⚡ Quick Entry Buttons:**")
        
        # Create columns for quick buttons (max 4 per row)
        quick_varieties = st.session_state.quick_buttons
        num_buttons = len(quick_varieties)
        
        if num_buttons > 0:
            # Calculate number of rows needed (max 4 buttons per row)
            buttons_per_row = min(4, num_buttons)
            rows = (num_buttons + buttons_per_row - 1) // buttons_per_row
            
            button_index = 0
            for row in range(rows):
                # Create columns for this row
                remaining_buttons = min(buttons_per_row, num_buttons - button_index)
                cols = st.columns(remaining_buttons)
                
                for col_idx in range(remaining_buttons):
                    if button_index < num_buttons:
                        variety_name = quick_varieties[button_index]
                        variety_info = df_var[df_var['name'] == variety_name]
                        
                        if not variety_info.empty:
                            variety_data = variety_info.iloc[0]
                            caffeine = int(variety_data.get('caffeine_mg', 0))
                            variety_id = int(variety_data['id'])
                            
                            with cols[col_idx]:
                                button_key = f"quick_{variety_name}_{button_index}"
                                if st.button(
                                    f"☕ {variety_name}\n({caffeine}mg)", 
                                    key=button_key,
                                    help=f"1 Tasse {variety_name} für heute hinzufügen",
                                    use_container_width=True
                                ):
                                    # Add entry for today with 1 cup of this variety
                                    today = date.today()
                                    with engine.begin() as conn:
                                        conn.execute(
                                            consumption.insert().values(
                                                date=today,
                                                cups=1,
                                                variety_id=variety_id
                                            )
                                        )
                                    st.success(f"✅ 1 Tasse {variety_name} für heute hinzugefügt! (+{caffeine}mg Koffein)")
                                    st.rerun()
                        
                        button_index += 1
            
            st.markdown("---")  # Separator between quick buttons and manual entry

with st.container():
    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
    
    with col1:
        entry_date = st.date_input("📅 Datum", max_value=date.today(), key="entry_date")
    with col2:
        entry_cups = st.number_input("☕ Anzahl Tassen", min_value=1, value=1, key="entry_cups")
    with col3:
        df_var = pd.read_sql(select(varieties), engine)
        if not df_var.empty:
            choice = st.selectbox("🌱 Sorte wählen", df_var['name'], key="entry_variety")
        else:
            st.warning("⚠️ Bitte erst eine Sorte in der Sidebar hinzufügen!")
            choice = None
            
    with col4:
        st.write("")  # Spacer for alignment
        submit_button = st.button("💾 Speichern", type="primary", use_container_width=True)
    
    # Show caffeine info when variety is selected - this updates in real-time
    if choice and not df_var.empty:
        selected_variety = df_var[df_var['name'] == choice].iloc[0]
        caffeine_per_cup = int(selected_variety.get('caffeine_mg', 0))
        total_caffeine_entry = entry_cups * caffeine_per_cup
        
        st.info(f"⚡ **{caffeine_per_cup}mg/Tasse** → Gesamt: **{total_caffeine_entry}mg** Koffein")
    
    # Handle form submission
    if submit_button and choice:
        vid = int(df_var[df_var['name'] == choice]['id'].iloc[0])
        caffeine_per_cup = int(df_var[df_var['name'] == choice]['caffeine_mg'].iloc[0])
        total_caffeine_entry = entry_cups * caffeine_per_cup
        
        with engine.begin() as conn:
            conn.execute(
                consumption.insert().values(
                    date=entry_date,
                    cups=entry_cups,
                    variety_id=vid
                )
            )
        st.success(f"✅ Eintrag erfolgreich gespeichert! (+{total_caffeine_entry}mg Koffein)")
        st.rerun()

# Einträge bearbeiten & löschen (optional)
if show_editor and not df.empty:
    st.markdown('<div class="section-header">✏️ Einträge bearbeiten & löschen</div>', unsafe_allow_html=True)
    
    # Display with caffeine info
    display_df = df[['id', 'date', 'cups', 'variety', 'caffeine_mg', 'total_caffeine']].copy()
    display_df = display_df.rename(columns={
        'caffeine_mg': 'Koffein/Tasse (mg)',
        'total_caffeine': 'Gesamt Koffein (mg)'
    })
    
    edited = st.data_editor(
        display_df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "date": st.column_config.DateColumn("📅 Datum"),
            "cups": st.column_config.NumberColumn("☕ Tassen", min_value=1),
            "variety": st.column_config.SelectboxColumn("🌱 Sorte"),
            "Koffein/Tasse (mg)": st.column_config.NumberColumn("⚡ Koffein/Tasse"),
            "Gesamt Koffein (mg)": st.column_config.NumberColumn("⚡ Gesamt Koffein")
        },
        disabled=["Koffein/Tasse (mg)", "Gesamt Koffein (mg)"]  # These are calculated fields
    )
    
    if st.button("💾 Änderungen übernehmen", type="primary"):
        # Convert back to original format for database operations
        edited_for_db = edited[['id', 'date', 'cups', 'variety']].copy()
        orig_ids = set(df['id'])
        new_ids = set(edited_for_db['id'])
        removed = orig_ids - new_ids
        with engine.begin() as conn:
            for rid in removed:
                conn.execute(consumption.delete().where(consumption.c.id == int(rid)))
        merged = edited_for_db.set_index('id').combine_first(df[['id', 'date', 'cups', 'variety']].set_index('id'))
        df_var = pd.read_sql(select(varieties), engine)
        with engine.begin() as conn:
            for idx, row in merged.iterrows():
                orig = df[['id', 'date', 'cups', 'variety']].set_index('id').loc[idx]
                if not orig.equals(row):
                    vid = int(df_var[df_var['name'] == row['variety']]['id'].iloc[0])
                    conn.execute(
                        consumption.update()
                                   .where(consumption.c.id == int(idx))
                                   .values(
                                       date=row['date'],
                                       cups=int(row['cups']),
                                       variety_id=vid
                                   )
                    )
        st.success("✅ Datenbank erfolgreich aktualisiert!")
        st.rerun()

# Zeitraum & Statistik-Basis
if show_stats and not df.empty:
    st.markdown('<div class="section-header">📊 Statistiken & Auswertungen</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        timeframe = st.selectbox(
            "🗓️ Zeitraum auswählen",
            ["Letzte 7 Tage", "Letzte 30 Tage", "Letzte 90 Tage", "Alles"]
        )
    
    today = pd.to_datetime(date.today())
    tmp = df.copy()
    if timeframe != "Alles":
        days = int(timeframe.split()[1])
        cutoff = today - pd.Timedelta(days=days-1)
        tmp = tmp[tmp['date'] >= cutoff]

    # Verbesserter Daily Chart mit Koffein
    if not tmp.empty:
        daily = tmp.groupby('date', as_index=False).agg({
            'cups': 'sum',
            'total_caffeine': 'sum'
        }).sort_values('date')
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 📈 Täglicher Kaffeekonsum")
            st.bar_chart(
                data=daily.rename(columns={'date':'Datum','cups':'Tassen'}), 
                x='Datum', 
                y='Tassen',
                color="#8B4513"
            )
        
        with col_chart2:
            st.markdown("### ⚡ Täglicher Koffeinkonsum")
            st.bar_chart(
                data=daily.rename(columns={'date':'Datum','total_caffeine':'Koffein (mg)'}), 
                x='Datum', 
                y='Koffein (mg)',
                color="#FF6B35"
            )
    else:
        st.info("📊 Keine Daten für den ausgewählten Zeitraum vorhanden.")

    # Layout für Pie Chart und Heatmap
    chart_col1, chart_col2 = st.columns(2)
    
    # Sorten-Verteilung (optional)
    if show_pie:
        with chart_col1:
            st.markdown("### 🥧 Sorten-Verteilung")
            pie = tmp.groupby('variety')['cups'].sum()
            if not pie.empty:
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                fig1.patch.set_facecolor('#f0f0f0')
                
                colors = plt.cm.Set3(range(len(pie)))
                wedges, texts, autotexts = ax1.pie(
                    pie, 
                    labels=pie.index, 
                    autopct='%1.1f%%', 
                    startangle=90,
                    colors=colors,
                    shadow=True,
                    explode=[0.05] * len(pie)
                )
                
                # Styling für bessere Lesbarkeit
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                
                ax1.axis('equal')
                plt.title('Verteilung nach Kaffeesorten', fontsize=14, fontweight='bold', pad=20)
                st.pyplot(fig1, use_container_width=True)
            else:
                st.info("🥧 Keine Sortendaten verfügbar.")

    # Kalender-Heatmap (optional)
    if show_heatmap:
        with chart_col2:
            st.markdown("### 🗓️ Kalender-Heatmap")
            tmp_series = tmp.groupby('date')['cups'].sum()

            if tmp_series.sum() == 0:
                st.info("🗓️ Keine Konsumdaten für die Heatmap vorhanden.")
            else:
                fig3, axes3 = calplot.calplot(
                    tmp_series,
                    how='sum',
                    fillcolor='lightgrey',
                    linewidth=0.5,
                    figsize=(10, 4),
                    cmap='YlOrBr'
                )
                fig3.suptitle("☕ Kaffeekonsum-Heatmap", fontsize=14, fontweight='bold')
                st.pyplot(fig3, use_container_width=True)

# Koffein-spezifische Statistiken (optional)
if show_caffeine and not df.empty:
    st.markdown('<div class="section-header">⚡ Koffein-Analyse</div>', unsafe_allow_html=True)
    
    today = pd.to_datetime(date.today())
    tmp = df.copy()
    if timeframe != "Alles":
        days = int(timeframe.split()[1])
        cutoff = today - pd.Timedelta(days=days-1)
        tmp = tmp[tmp['date'] >= cutoff]
    
    if not tmp.empty:
        col1, col2, col3 = st.columns(3)
        
        avg_daily_caffeine = tmp.groupby('date')['total_caffeine'].sum().mean()
        max_daily_caffeine = tmp.groupby('date')['total_caffeine'].sum().max()
        high_caffeine_days = len(tmp.groupby('date')['total_caffeine'].sum()[lambda x: x > 400])
        
        with col1:
            st.metric("📊 Ø Koffein/Tag", f"{avg_daily_caffeine:.0f}mg")
        with col2:
            st.metric("📈 Max Koffein/Tag", f"{max_daily_caffeine:.0f}mg")
        with col3:
            st.metric("⚠️ Tage >400mg", f"{high_caffeine_days}")
        
        # Koffein nach Sorten
        st.markdown("### ⚡ Koffein nach Sorten")
        caffeine_by_variety = tmp.groupby('variety').agg({
            'total_caffeine': 'sum',
            'cups': 'sum',
            'caffeine_mg': 'first'
        }).sort_values('total_caffeine', ascending=False)
        
        caffeine_by_variety['avg_per_cup'] = caffeine_by_variety['caffeine_mg']
        caffeine_by_variety = caffeine_by_variety.rename(columns={
            'total_caffeine': 'Gesamt Koffein (mg)',
            'cups': 'Anzahl Tassen',
            'avg_per_cup': 'Koffein/Tasse (mg)'
        })
        
        st.dataframe(caffeine_by_variety, use_container_width=True)
        
        # Koffein-Heatmap
        st.markdown("### 🗓️ Koffein-Heatmap")
        caffeine_series = tmp.groupby('date')['total_caffeine'].sum()
        
        if caffeine_series.sum() > 0:
            fig4, axes4 = calplot.calplot(
                caffeine_series,
                how='sum',
                fillcolor='lightgrey',
                linewidth=0.5,
                figsize=(10, 4),
                cmap='Reds'
            )
            fig4.suptitle("⚡ Koffeinkonsum-Heatmap (mg)", fontsize=14, fontweight='bold')
            st.pyplot(fig4, use_container_width=True)

# Import / Export CSV (optional)
if show_import:
    st.markdown('<div class="section-header">📁 Import & Export</div>', unsafe_allow_html=True)
    col_imp, col_exp = st.columns(2)
    
    with col_imp:
        st.markdown("#### 📥 Import")
        up1 = st.file_uploader("🌱 Varieties CSV importieren", type=['csv'])
        if up1:
            dfv = pd.read_csv(up1)
            with engine.begin() as conn:
                conn.execute(varieties.insert(), dfv.to_dict(orient='records'))
            st.success("✅ Sorten erfolgreich importiert!")
            
        up2 = st.file_uploader("☕ Consumption CSV importieren", type=['csv'])
        if up2:
            dfc = pd.read_csv(up2, parse_dates=['date'])
            df_var = pd.read_sql(select(varieties), engine)
            dfc = dfc.merge(df_var, how='left', left_on='variety', right_on='name')
            to_ins = dfc[['date','cups','id']].rename(columns={'id':'variety_id'}).to_dict(orient='records')
            with engine.begin() as conn:
                conn.execute(consumption.insert(), to_ins)
            st.success("✅ Einträge erfolgreich importiert!")
            
    with col_exp:
        st.markdown("#### 📤 Export")
        all_var = pd.read_sql(select(varieties), engine)
        buf1 = io.StringIO()
        all_var.to_csv(buf1, index=False)
        st.download_button("🌱 Varieties exportieren", buf1.getvalue(), "varieties.csv", "text/csv")
        
        all_cons = pd.read_sql(
            "SELECT c.*, v.name AS variety FROM consumption c JOIN varieties v ON c.variety_id=v.id",
            engine, parse_dates=['date']
        )
        buf2 = io.StringIO()
        all_cons.to_csv(buf2, index=False)
        st.download_button("☕ Consumption exportieren", buf2.getvalue(), "consumption.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #8B4513; font-style: italic;">Made with ☕ and ❤️</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="text-align: center; color: #8B4513; font-style: italic;">by <a href="https://github.com/cancel-cloud" style="color: #8B4513;">Lukas</a></div>',
    unsafe_allow_html=True
)