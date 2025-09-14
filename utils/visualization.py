import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def generate_all_visualizations(df):
    visuals = {}

    def save_plot(fig, title):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close(fig)
        return img_base64

    try:
        # Correlation Heatmap
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
        visuals["correlation_heatmap"] = save_plot(fig, "Correlation Heatmap")
    except Exception as e:
        visuals["correlation_heatmap"] = f"⚠️ Could not generate heatmap: {e}"

    try:
        # Distribution of first numeric column
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) > 0:
            fig, ax = plt.subplots()
            sns.histplot(df[num_cols[0]], kde=True, ax=ax)
            visuals[f"{num_cols[0]}_distribution"] = save_plot(fig, f"{num_cols[0]} Distribution")
    except Exception as e:
        visuals["distribution"] = f"⚠️ Could not generate distribution: {e}"

    return visuals
