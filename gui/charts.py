import matplotlib.pyplot as plt
import matplotlib
import pygame
import io

# Use Agg backend for non-interactive plot generation
matplotlib.use('Agg')

def create_benchmark_chart(data, width=320, height=200):
    """
    data: Dict { 'A*': value, 'BFS': value, 'UCS': value }
    Returns: pygame.Surface
    """
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    
    algos = list(data.keys())
    values = list(data.values())
    
    # Matching Theme.PRIMARY (Teal/Green), Theme.DANGER (Red), Theme.ACCENT (Yellow)
    colors = ['#22C55E', '#EF4444', '#EAB308'] 
    bars = ax.bar(algos, values, color=colors[:len(algos)], alpha=0.9, width=0.6)
    
    ax.set_title("Search Efficiency (Nodes Explored)", fontsize=11, color='#F8FAFC', pad=15)
    ax.set_ylabel("Nodes", fontsize=9, color='#94A3B8')
    ax.tick_params(axis='both', which='major', labelsize=9, colors='#94A3B8')
    
    # Hide top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363D')
    ax.spines['bottom'].set_color('#30363D')
    
    # Transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    
    plot_surf = pygame.image.load(buf)
    plt.close(fig)
    return plot_surf
