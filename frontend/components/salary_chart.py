import streamlit as st
import matplotlib.pyplot as plt
import io

def render_salary_chart(min_sal: int, max_sal: int, currency: str = "USD"):
    """
    Renders a clean horizontal bar showing the salary range bounds.
    """
    if min_sal == 0 or max_sal == 0:
        st.write("Compensation range not available.")
        return
        
    fig, ax = plt.subplots(figsize=(6, 1.2))
    
    # Hide axes ticks and frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.get_yaxis().set_visible(False)
    
    # Plotting range as a thick bar
    ax.barh(0.5, max_sal - min_sal, left=min_sal, height=0.3, color='#3B82F6', alpha=0.9, edgecolor='none', label='Estimated Range')
    
    # Set limits with padding
    ax.set_xlim(min_sal * 0.85, max_sal * 1.1)
    ax.set_ylim(0, 1)
    
    # Format x-axis as currency
    import matplotlib.ticker as ticker
    formatter = ticker.FuncFormatter(lambda x, pos: f'${int(x/1000)}k')
    ax.xaxis.set_major_formatter(formatter)
    
    # Add text labels on ends
    ax.text(min_sal, 0.75, f"${min_sal:,}", ha='center', va='center', fontweight='bold', color='#1E3A8A', fontsize=10)
    ax.text(max_sal, 0.75, f"${max_sal:,}", ha='center', va='center', fontweight='bold', color='#1E3A8A', fontsize=10)
    
    plt.tight_layout()
    
    # Convert to image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, transparent=True)
    buf.seek(0)
    
    st.image(buf, use_container_width=True)
    plt.close(fig)
