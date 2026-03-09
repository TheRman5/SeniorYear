import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file without headers since the format is custom
df = pd.read_csv('MasterExperiment.csv', header=None)

# Function to extract experiment data
def extract_experiments(df):
    experiments = {}
    current_exp = None
    
    for idx, row in df.iterrows():
        # Check if this is an experiment header
        if pd.notna(row.iloc[0]) and str(row.iloc[0]).startswith('Experiment #:'):
            current_exp = int(row.iloc[1])
            experiments[current_exp] = {'Lambda': [], 'Lambda_t': [], 'H': [], 'H_t': [], 'Class': []}
        # Check if this is a data row (has Step column filled and not header)
        elif current_exp is not None and pd.notna(row.iloc[0]) and row.iloc[0] != 'Step':
            try:
                step = int(row.iloc[0])
                class_val = row.iloc[2]
                lambda_val = row.iloc[3]
                lambda_t_val = row.iloc[4]
                h_val = row.iloc[5]
                h_t_val = row.iloc[6]
                
                # Only add if we have valid data
                if pd.notna(class_val) and pd.notna(lambda_val):
                    # Convert class to behavior value: 0 for classes I and II, 1 for class IV, 2 for class III
                    class_int = int(class_val)
                    if class_int in [1, 2]:
                        behavior = 0
                    elif class_int == 4:
                        behavior = 1
                    elif class_int == 3:
                        behavior = 2
                    else:
                        continue
                    
                    experiments[current_exp]['Lambda'].append(float(lambda_val))
                    experiments[current_exp]['Lambda_t'].append(float(lambda_t_val))
                    experiments[current_exp]['H'].append(float(h_val))
                    experiments[current_exp]['H_t'].append(float(h_t_val))
                    experiments[current_exp]['Class'].append(behavior)
            except (ValueError, TypeError):
                continue
    
    return experiments

# Extract all experiments
experiments = extract_experiments(df)

# Create the four plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Behavior vs. Parameters Across All Experiments', fontsize=16, y=1.00)

# Define colors for different experiments (using a colormap)
colors = plt.cm.tab20(np.linspace(0, 1, len(experiments)))

# Plot configurations
plots = [
    ('Lambda', 'λ', axes[0, 0]),
    ('Lambda_t', 'λT', axes[0, 1]),
    ('H', 'H', axes[1, 0]),
    ('H_t', 'HT', axes[1, 1])
]

for param, label, ax in plots:
    for i, (exp_num, data) in enumerate(sorted(experiments.items())):
        if len(data[param]) > 0:
            ax.plot(data[param], data['Class'], 
                   marker='o', linestyle='', markersize=5,
                   color=colors[i % len(colors)], 
                   label=f'Exp {exp_num}', alpha=0.7)
    
    ax.set_xlabel(label, fontsize=12, fontweight='bold')
    ax.set_ylabel('Behavior', fontsize=12, fontweight='bold')
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['Classes I & II', 'Class IV', 'Class III'])
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Behavior vs. {label}', fontsize=13, fontweight='bold')

# Add a single legend for all experiments (placed outside the plots)
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1.0, 0.5), 
          ncol=1, fontsize=8, title='Experiments')

plt.tight_layout(rect=[0, 0, 0.95, 0.98])
plt.savefig('behavior_graphs.png', dpi=300, bbox_inches='tight')
print("Graphs saved as 'behavior_graphs.png'")
plt.show()
