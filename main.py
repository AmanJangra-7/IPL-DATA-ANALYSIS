import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

warnings.filterwarnings('ignore')

# ============================================================
# STYLE SETTINGS
# ============================================================

plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor':   '#FAFAFA',
    'axes.edgecolor':   '#CCCCCC',
    'axes.grid':        True,
    'grid.color':       '#E8E8E8',
    'grid.linewidth':   0.8,
    'font.family':      'DejaVu Sans',
    'font.size':        11,
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
    'axes.labelsize':   11,
    'xtick.labelsize':  10,
    'ytick.labelsize':  10,
})

BLUE   = '#378ADD'
GREEN  = '#639922'
AMBER  = '#BA7517'
CORAL  = '#D85A30'
PURPLE = '#7F77DD'
GRAY   = '#888780'

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _bar_labels(ax, fmt='{:.0f}', color='#444441', pad=3):
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                fmt.format(h),
                xy=(p.get_x() + p.get_width() / 2, h),
                xytext=(0, pad),
                textcoords='offset points',
                ha='center',
                va='bottom',
                fontsize=9,
                color=color
            )


def _hbar_labels(ax, fmt='{:.0f}', color='#444441', pad=3):
    for p in ax.patches:
        w = p.get_width()
        if w > 0:
            ax.annotate(
                fmt.format(w),
                xy=(w, p.get_y() + p.get_height() / 2),
                xytext=(pad, 0),
                textcoords='offset points',
                ha='left',
                va='center',
                fontsize=9,
                color=color
            )

# ============================================================
# 1. PLAYER OF MATCH
# ============================================================

def plot_player_of_match(df, top_n=15):

    pom = df['player_of_match'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(pom.index[::-1], pom.values[::-1],
            color=BLUE,
            height=0.65)

    _hbar_labels(ax)

    ax.set_xlabel('Number of awards')
    ax.set_title(f'Top {top_n} Player of Match Awards')

    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

# ============================================================
# 2. TOP RUN SCORERS
# ============================================================

def plot_top_run_scorers(deliveries_df, top_n=15):

    bat_col = 'batsman' if 'batsman' in deliveries_df.columns else 'batter'
    run_col = 'batsman_runs' if 'batsman_runs' in deliveries_df.columns else 'total_runs'

    runs = deliveries_df.groupby(bat_col)[run_col] \
                        .sum() \
                        .sort_values(ascending=False) \
                        .head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(runs.index[::-1],
            runs.values[::-1],
            color=GREEN)

    _hbar_labels(ax)

    ax.set_xlabel('Runs')
    ax.set_title('Top Run Scorers')

    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

# ============================================================
# 3. TOP WICKET TAKERS
# ============================================================

def plot_top_wicket_takers(deliveries_df, top_n=15):

    non_bowler = [
        'run out',
        'retired hurt',
        'obstructing the field',
        'retired out'
    ]

    wickets_df = deliveries_df[
        deliveries_df['dismissal_kind'].notna() &
        ~deliveries_df['dismissal_kind'].str.lower().isin(non_bowler)
    ]

    wickets = wickets_df.groupby('bowler') \
                        .size() \
                        .sort_values(ascending=False) \
                        .head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(wickets.index[::-1],
            wickets.values[::-1],
            color=CORAL)

    _hbar_labels(ax)

    ax.set_xlabel('Wickets')
    ax.set_title('Top Wicket Takers')

    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

# ============================================================
# 4. TEAM PERFORMANCE
# ============================================================

def plot_team_performance(df):

    teams = set(df['team1']) | set(df['team2'])

    rows = []

    for team in teams:

        played = len(df[
            (df['team1'] == team) |
            (df['team2'] == team)
        ])

        won = len(df[df['winner'] == team])

        win_pct = (won / played) * 100 if played else 0

        rows.append((team, win_pct))

    rows.sort(key=lambda x: x[1])

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(labels, values, color=AMBER)

    _hbar_labels(ax, fmt='{:.1f}%')

    ax.set_xlabel('Win Percentage')
    ax.set_title('Team Performance')

    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

# ============================================================
# 5. TOSS ANALYSIS
# ============================================================

def plot_toss_analysis(df):

    valid = df.dropna(subset=['toss_winner', 'winner'])

    toss_won = (valid['toss_winner'] == valid['winner']).sum()
    toss_lost = len(valid) - toss_won

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        [toss_won, toss_lost],
        labels=['Won Match', 'Lost Match'],
        colors=[BLUE, GRAY],
        autopct='%1.1f%%'
    )

    ax.set_title('Toss Impact Analysis')

    plt.show()

# ============================================================
# 6. SEASON STATS
# ============================================================

def plot_season_stats(df):

    seasons = sorted(df['season'].unique())

    match_counts = []

    for s in seasons:
        match_counts.append(len(df[df['season'] == s]))

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        [str(s) for s in seasons],
        match_counts,
        color=BLUE
    )

    _bar_labels(ax)

    ax.set_xlabel('Season')
    ax.set_ylabel('Matches')

    ax.set_title('Season Wise Match Count')

    plt.tight_layout()
    plt.show()

# ============================================================
# 7. HEAD TO HEAD
# ============================================================

def plot_head_to_head(df, min_matches=5):

    pairs = {}

    for _, row in df.iterrows():

        t1 = row['team1']
        t2 = row['team2']
        winner = row['winner']

        key = tuple(sorted([t1, t2]))

        if key not in pairs:
            pairs[key] = {
                t1: 0,
                t2: 0,
                'total': 0
            }

        pairs[key]['total'] += 1

        if winner in pairs[key]:
            pairs[key][winner] += 1

    labels = []
    values1 = []
    values2 = []

    for (t1, t2), val in pairs.items():

        if val['total'] >= min_matches:

            labels.append(f"{t1} vs {t2}")

            values1.append((val[t1] / val['total']) * 100)
            values2.append((val[t2] / val['total']) * 100)

    fig, ax = plt.subplots(figsize=(12, 8))

    y = np.arange(len(labels))

    ax.barh(y, values1, color=BLUE, label='Team 1')
    ax.barh(y, values2, left=values1, color=GREEN, label='Team 2')

    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    ax.set_xlabel('Win Share %')

    ax.set_title('Head to Head Win Share')

    ax.legend()

    plt.tight_layout()
    plt.show()

# ============================================================
# 8. VENUE ANALYSIS
# ============================================================

def plot_venue_analysis(df, top_n=10):

    top_venues = df['venue'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        top_venues.index,
        top_venues.values,
        color=PURPLE
    )

    _bar_labels(ax)

    ax.set_xticklabels(top_venues.index,
                       rotation=40,
                       ha='right')

    ax.set_title('Top IPL Venues')

    plt.tight_layout()
    plt.show()

# ============================================================
# 9. BATTING SCATTER
# ============================================================

def plot_batting_scatter(deliveries_df):

    bat_col = 'batsman' if 'batsman' in deliveries_df.columns else 'batter'
    run_col = 'batsman_runs' if 'batsman_runs' in deliveries_df.columns else 'total_runs'

    runs = deliveries_df.groupby(bat_col)[run_col].sum()
    balls = deliveries_df.groupby(bat_col).size()

    strike_rate = (runs / balls) * 100

    top_players = runs.sort_values(ascending=False).head(20)

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        balls[top_players.index],
        top_players.values,
        c=strike_rate[top_players.index],
        cmap='RdYlGn',
        s=120
    )

    for player in top_players.index:
        ax.annotate(
            player,
            (balls[player], top_players[player]),
            fontsize=8
        )

    plt.colorbar(scatter, ax=ax, label='Strike Rate')

    ax.set_xlabel('Balls Faced')
    ax.set_ylabel('Runs')
    ax.set_title('Batting Analysis Scatter Plot')

    plt.tight_layout()
    plt.show()

# ============================================================
# IPL ANALYZER CLASS
# ============================================================

class IPLAnalyzer:

    def __init__(self):

        self.data_loaded = False
        self.matches_df = None
        self.deliveries_df = None

    def load_data(self):

        try:

            self.matches_df = pd.read_csv('matches.csv')
            self.deliveries_df = pd.read_csv('deliveries.csv')

            self.data_loaded = True

            print("IPL Data Loaded Successfully")

        except Exception as e:

            print("Error Loading Data")
            print(e)

# ============================================================
# LOAD DATA
# ============================================================

analyzer = IPLAnalyzer()
analyzer.load_data()

if not analyzer.data_loaded:
    exit()

# ============================================================
# GUI WINDOW
# ============================================================

root = tk.Tk()

root.title("IPL Data Analysis Dashboard")
root.geometry("500x650")
root.configure(bg="#f5f5f5")

title = tk.Label(
    root,
    text="IPL DATA ANALYSIS",
    font=("Arial", 18, "bold"),
    bg="#f5f5f5",
    fg="#222"
)

title.pack(pady=20)

# ============================================================
# SEASON SELECTOR
# ============================================================

season_label = tk.Label(
    root,
    text="Select IPL Season",
    font=("Arial", 12, "bold"),
    bg="#f5f5f5"
)

season_label.pack()

all_seasons = sorted(
    analyzer.matches_df['season']
    .dropna()
    .unique()
    .astype(int)
    .tolist()
)

season_options = ["All Years"] + [str(s) for s in all_seasons]

season_var = tk.StringVar()
season_var.set("All Years")

season_dropdown = ttk.Combobox(
    root,
    textvariable=season_var,
    values=season_options,
    state="readonly",
    width=25
)

season_dropdown.pack(pady=10)

# ============================================================
# VISUALIZATION SELECTOR
# ============================================================

visual_label = tk.Label(
    root,
    text="Select Visualization",
    font=("Arial", 12, "bold"),
    bg="#f5f5f5"
)

visual_label.pack(pady=10)

visualizations = {
    "1. Player of Match": 1,
    "2. Top Run Scorers": 2,
    "3. Top Wicket Takers": 3,
    "4. Team Performance": 4,
    "5. Toss Analysis": 5,
    "6. Season Statistics": 6,
    "7. Head To Head": 7,
    "8. Venue Analysis": 8,
    "9. Batting Scatter": 9
}

selected_option = tk.StringVar()
selected_option.set("1. Player of Match")

option_menu = ttk.Combobox(
    root,
    textvariable=selected_option,
    values=list(visualizations.keys()),
    state="readonly",
    width=35
)

option_menu.pack(pady=10)

# ============================================================
# GENERATE VISUALIZATION
# ============================================================

def generate_visualization():

    selected_season = season_var.get()
    selected_plot = visualizations[selected_option.get()]

    if selected_season == "All Years":

        current_mdf = analyzer.matches_df
        current_ddf = analyzer.deliveries_df

    else:

        selected_season = int(selected_season)

        current_mdf = analyzer.matches_df[
            analyzer.matches_df['season'] == selected_season
        ]

        match_ids = current_mdf['id'].unique()

        current_ddf = analyzer.deliveries_df[
            analyzer.deliveries_df['match_id'].isin(match_ids)
        ]

    try:

        if selected_plot == 1:
            plot_player_of_match(current_mdf)

        elif selected_plot == 2:
            plot_top_run_scorers(current_ddf)

        elif selected_plot == 3:
            plot_top_wicket_takers(current_ddf)

        elif selected_plot == 4:
            plot_team_performance(current_mdf)

        elif selected_plot == 5:
            plot_toss_analysis(current_mdf)

        elif selected_plot == 6:
            plot_season_stats(current_mdf)

        elif selected_plot == 7:
            plot_head_to_head(current_mdf)

        elif selected_plot == 8:
            plot_venue_analysis(current_mdf)

        elif selected_plot == 9:
            plot_batting_scatter(current_ddf)

        messagebox.showinfo(
            "Success",
            "Visualization Generated Successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

# ============================================================
# BUTTON
# ============================================================

generate_btn = tk.Button(
    root,
    text="Generate Visualization",
    font=("Arial", 12, "bold"),
    bg="#378ADD",
    fg="white",
    padx=15,
    pady=10,
    command=generate_visualization
)

generate_btn.pack(pady=30)

# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="IPL Dashboard using Python",
    bg="#f5f5f5",
    fg="gray"
)

footer.pack(side="bottom", pady=15)

# ============================================================
# RUN GUI
# ============================================================

root.mainloop()