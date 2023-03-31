import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib
import seaborn as sns
import pandas as pd


PARTY_COLORS = {
    "SPD": "#E3000F",
    "CSU/CDU": "#000000",
    "Bündnis 90/Die Grünen": "#1AA037",
    "Die Linke": "#800080",
    "FDP": "#FFEF00",
    "AfD": "#0489DB",
}

REG_COLORS = {
    "Government": "#E3000F",
    "Opposition": "#0489DB",
}

PARTY_ORDER = ["SPD", "CSU/CDU", "Bündnis 90/Die Grünen", "FDP", "AfD", "Die Linke"]
REG_ORDER = ["Government", "Opposition"]
POSITIVE_COLOR = "#76B041"  # "#006600"
NEGATIVE_COLOR = "#E4572E"  # "#FF0000"
NEUTRAL_COLOR = "#2E282A"  # "#999999"

FONT_PATH = "fonts/manrope-regular.otf"  #'fonts/LinLibertine_R.ttf'

# Global Plot Settings
sns.set(rc={"figure.dpi": 300})
sns.set(rc={"figure.figsize": (6, 3)})


def setup_font(plt):
    # font_manager.fontManager.addfont(FONT_PATH)
    # prop = font_manager.FontProperties(fname=FONT_PATH)

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams.update({"font.size": 14})
    # plt.rcParams['font.sans-serif'] = prop.get_name()
    return plt

POSITIVE_COLOR = "#76B041"  # "#006600"
NEGATIVE_COLOR = "#E4572E"  # "#FF0000"
NEUTRAL_COLOR = "#2E282A"  # "#999999"

def plot_percentage(df, filename):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style("whitegrid")

    # Setup Font
    plt = setup_font(plt)
    df["Partei"] = df["Partei"].replace({"Bündnis 90/Die Grünen": "Die Grünen"})
    # Group the data by party and sentiment, unstack to create a table
    data = df.groupby(["Partei"])["model_predictions"].value_counts().unstack()
    # Normalize the data so that each column sums to 100
    data = data.div(data.sum(axis=1), axis=0).mul(100)
    # Round values to 1 decimal place
    data = data.applymap(lambda x: round(x, 1))
    data = data.rename(columns={0: "NOT", 1: "HOF"})

    # Get the overall sentiment values
    combined_data = df["Label"].value_counts()
    # Format the data as a DataFrame and normalize
    combined_data = (
        pd.DataFrame(combined_data).T.rename(index={"Label": "Combined"})
        / combined_data.sum()
        * 100
    )
    # Round the values to 1 decimal place
    combined_data = combined_data.applymap(lambda x: round(x, 1))
    
    # Combine the total and party-specific data
    data_total = pd.concat([combined_data, data], axis=0)
    # Reorder columns
    data_total = data_total[["HOF", "NOT"]]

    data_total = data_total.reindex(
        ["Combined", "SPD", "CSU/CDU", "Die Grünen", "FDP", "AfD", "Die Linke"]
    )

    # Create chart
    ax = data_total.plot(
        kind="bar",
        stacked=True,
        color=[NEUTRAL_COLOR, NEGATIVE_COLOR],
        width=0.8,
    )

    for c in ax.containers:
        # Add custom label to the bars
        ax.bar_label(c, label_type="center", color="white", fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(
         reversed(handles),
         reversed(labels),
         loc="center left",
         bbox_to_anchor=(1, 0.5),
         #title="HOF (1) vs. NOT (0)",
     )
    # Remove legend
    #ax.get_legend().remove()
    plt.xticks(fontsize=8,rotation=0)
    plt.ylabel("Proportion in %", fontsize=18)
    plt.xlabel("Party", fontsize=18)

    # Save as svg, png and pdf
    for f_type in [".png"]:
        plt.savefig(filename + f_type, dpi=300, bbox_inches="tight")

    plt.show()


def plot_line_graph_for_each_day(df, filename):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.dates as mdates

    sns.set_style("whitegrid")

    # Setup Font
    plt = setup_font(plt)

    _, ax = plt.subplots(figsize=(15, 6))

    # Set figure size and font size
    # plt.figure(figsize=(15, 6))
    plt.rcParams.update({"font.size": 16})

    # Plot the sentiment value for each party and month
    for party in PARTY_ORDER:
        ax.plot(
            df.loc[df["Partei"] == party, "day"],
            df.loc[df["Partei"] == party, "model_predictions"],
            label=party,
            color=PARTY_COLORS[party],
        )

    # Set x-axis tick labels
   # plt.xticks()
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    # Add legend, axis labels and title
    legend = ax.legend(loc="upper left", title="Party", ncol=2)
    legend._legend_box.align = "left"
    plt.xlabel("Date", fontsize=18, labelpad=15)
    plt.ylabel("Mean HOF", x=-2, fontsize=18, labelpad=15)

    plt.grid(alpha=0.5)

    # Add labels for the positive and negative y-axis directions
    plt.text(
        -0.07,
        0.85,
        "HOF →",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=POSITIVE_COLOR,
    )
    plt.text(
        -0.07,
        0.15,
        "← NOT",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=NEGATIVE_COLOR,
    )

    # Set y-axis limit
    plt.ylim(0, 0.45)

    # Save as svg, png and pdf
    for f_type in [".png"]:
        plt.savefig(filename + f_type, dpi=300, bbox_inches="tight")

    plt.show()

    
def plot_reg_line_graph_for_each_day(df, filename):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.dates as mdates

    sns.set_style("whitegrid")

    # Setup Font
    plt = setup_font(plt)

    _, ax = plt.subplots(figsize=(15, 6))

    # Set figure size and font size
    # plt.figure(figsize=(15, 6))
    plt.rcParams.update({"font.size": 16})

    # Plot the sentiment value for each party and month
    for party in REG_ORDER:
        ax.plot(
            df.loc[df["Regierungsstatus_2021"] == party, "day"],
            df.loc[df["Regierungsstatus_2021"] == party, "model_predictions"],
            label=party,
            color=REG_COLORS[party],
        )

    # Set x-axis tick labels
   # plt.xticks()
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    # Add legend, axis labels and title
    legend = ax.legend(loc="upper left", title="Government status", ncol=1)
    legend._legend_box.align = "left"
    plt.xlabel("Date", fontsize=18, labelpad=15)
    plt.ylabel("Mean HOF", x=-2, fontsize=18, labelpad=15)

    plt.grid(alpha=0.5)

    # Add labels for the positive and negative y-axis directions
    plt.text(
        -0.07,
        0.85,
        "HOF →",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=POSITIVE_COLOR,
    )
    plt.text(
        -0.07,
        0.15,
        "← NOT",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=NEGATIVE_COLOR,
    )

    # Set y-axis limit
    plt.ylim(0.10, 0.35)

    # Save as svg, png and pdf
    for f_type in [".png"]:
        plt.savefig(filename + f_type, dpi=300, bbox_inches="tight")

    plt.show()
    
def plot_gender_percentage(df, filename):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style("whitegrid")

    # Setup Font
    plt = setup_font(plt)
    #df["Partei"] = df["Partei"].replace({"Bündnis 90/Die Grünen": "Die Grünen"})
    # Group the data by party and sentiment, unstack to create a table
    data = df.groupby(["Geschlecht"])["model_predictions"].value_counts().unstack()
    # Normalize the data so that each column sums to 100
    data = data.div(data.sum(axis=1), axis=0).mul(100)
    # Round values to 1 decimal place
    data = data.applymap(lambda x: round(x, 1))
    #data = data.rename(columns={0: "NOT", 1: "HOF"})
    
    # Get the overall sentiment values
    combined_data = df["model_predictions"].value_counts()
    # Format the data as a DataFrame and normalize
    combined_data = (
        pd.DataFrame(combined_data).T.rename(index={"Label": "Combined"})
        / combined_data.sum()
        * 100
    )
    # Round the values to 1 decimal place
    combined_data = combined_data.applymap(lambda x: round(x, 1))
    
    # Combine the total and party-specific data
    data_total = pd.concat([combined_data, data], axis=0)
    # Reorder columns

    print(data_total.head())
    data_total = data_total[[1, 0]]
    data_total = data_total.rename(columns={0: "NOT", 1: "HOF"})
    data_total = data_total.reindex(
        ["Frau","Herrn"]
    )

    # Create chart
    ax = data_total.plot(
        kind="bar",
        stacked=True,
        color=[NEUTRAL_COLOR, NEGATIVE_COLOR],
        width=0.8,
    )

    for c in ax.containers:
        # Add custom label to the bars
        ax.bar_label(c, label_type="center", color="white", fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(
         reversed(handles),
         reversed(labels),
         loc="center left",
         bbox_to_anchor=(1, 0.5),
         #title="HOF (1) vs. NOT (0)",
     )
    # Remove legend
    #ax.get_legend().remove()
    plt.xticks(fontsize=8,rotation=0)
    plt.ylabel("Proportion in %", fontsize=18)
    plt.xlabel("Gender", fontsize=18)

    # Save as svg, png and pdf
    for f_type in [".png"]:
        plt.savefig(filename + f_type, dpi=300, bbox_inches="tight")

    plt.show()

    
def plot_poli_line_graph_for_each_day(df, filename):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.dates as mdates

    sns.set_style("whitegrid")

    # Setup Font
    plt = setup_font(plt)

    _, ax = plt.subplots(figsize=(15, 6))

    # Set figure size and font size
    # plt.figure(figsize=(15, 6))
    plt.rcParams.update({"font.size": 16})

    # Plot the sentiment value for each party and month
    for party in PARTY_ORDER:
        ax.plot(
            df.loc[df["Partei"] == party, "month"],
            df.loc[df["Partei"] == party, "model_predictions"],
            label=party,
            color=PARTY_COLORS[party],
        )

    # Set x-axis tick labels
   # plt.xticks()
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.AutoDateLocator()) #interval = 1
        # set formatter
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter())

    # Add legend, axis labels and title
    legend = ax.legend(loc="upper left", title="Party", ncol=2)
    legend._legend_box.align = "left"
    plt.xlabel("Months of 2021", fontsize=18, labelpad=15)
    plt.ylabel("Mean HOF", x=-2, fontsize=18, labelpad=15)

    plt.grid(alpha=0.5)

    # Add labels for the positive and negative y-axis directions
    plt.text(
        -0.07,
        0.85,
        "HOF →",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=POSITIVE_COLOR,
    )
    plt.text(
        -0.07,
        0.15,
        "← NOT",
        transform=ax.transAxes,
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=14,
        color=NEGATIVE_COLOR,
    )

    # Set y-axis limit
    plt.ylim(0, 0.45)

    # Save as svg, png and pdf
    for f_type in [".png"]:
        plt.savefig(filename + f_type, dpi=300, bbox_inches="tight")

    plt.show()
