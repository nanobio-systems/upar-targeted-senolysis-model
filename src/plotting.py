import matplotlib.pyplot as plt, numpy as np
from types import SimpleNamespace

def plot_single(
    x, y, xlabel, ylabel, title, label=None
):
    plt.figure(figsize=(8,5))

    plt.plot(x, y, label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if label is not None:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show

def plot_comp(
    title, xlabel, ylabel, limit, *datasets
):
    plt.figure(figsize=(8,5))

    for i, dataset in enumerate(datasets):
        if hasattr(dataset, 'x'):
            x = dataset.x
            y = dataset.y[0]
            label = dataset.label
        else:
            x, y, label = dataset

        if title == "Senescent Intracellular Nanoparticle Loading: Saturable Endocytosis Profile":
            palette = ("#0072B2", "#56B4E9", "#D55E00", "#E69F00")
            colour = palette[i % len(palette)]
            linestyle = '--'
        else:
            linestyle = '-' if i in [0, 1, 4, 5] else '--'
            if i in range(0, 4):
                if i % 2 == 0:
                    colour = "#0072B2"
                else:
                    colour = "#56B4E9"
            else:
                if i % 2 == 0:
                    colour = "#D55E00"
                else:
                    colour = "#E69F00"
        plt.plot(x, y, label=label, color=colour, linestyle=linestyle)

        

    plt.xlim(0, limit)
    plt.ylim(0, None)

    if title == "Senescent Intracellular Nanoparticle Loading: Saturable Endocytosis Profile":
        plt.yscale('log')
        plt.ylim(1, 0.9e7)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def dev_comp(dataset1, dataset2, operation, labels=None):

    proc_datasets = []

    for item1, item2, label in zip(dataset1, dataset2, labels):

        def extract_data(obj):
            if not hasattr(obj, 't'):
                return None, None
            if hasattr(obj, 'y'):
                return obj.t, obj.y[0]
            elif hasattr(obj, 'P'):
                return obj.t, obj.P
            return None, None

        t_1raw, val_1 = extract_data(item1)
        t_2raw, val_2 = extract_data(item2)

        t_1 = t_1raw / 3600.0 if t_1raw is not None else None
        t_2 = t_2raw / 3600.0 if t_2raw is not None else None

        if hasattr(item1, 'y') and not hasattr(item1, 'P'):
            p_t, y_a = t_1, val_1
            l_t, l_val = t_2, val_2
        elif hasattr(item2, 'y') and not hasattr(item2, 'P'):
            p_t, y_a = t_2, val_2
            l_t, l_val = t_1, val_1
        else:
            p_t, y_a = t_1, val_1
            l_t, l_val = t_2, val_2

        if y_a is None or l_val is None:
            raise AttributeError("Could not resolve valid 'y[0]' or 'P' attributes on the inputs.")

        y_b = np.interp(p_t, l_t, l_val)

        if operation == "div":
            calc_y = np.divide(y_a, y_b, out=np.zeros_like(y_b, dtype=float), where=y_b != 0)
        elif operation == "sub":
            calc_y = y_a - y_b
        elif operation == "mul":
            calc_y = y_a * y_b
        elif operation == "add":
            calc_y = y_a + y_b
        else:
            raise ValueError(f"Unknown operation: {operation}")

        comp_set = SimpleNamespace(x=p_t, y=[calc_y], label=label)
        proc_datasets.append(comp_set)

    return proc_datasets
    
# also look at producing a good looking table through this and/or through markdown cells formatting...