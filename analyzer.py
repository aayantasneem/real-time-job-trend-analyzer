import pandas as pd

def analyze_jobs(filename="jobs.csv"):
    try:
        df = pd.read_csv(filename)

        df["publication_date"] = pd.to_datetime(df["date"], errors="coerce")

        df.dropna(subset=["publication_date"], inplace=True)

        daily_counts = df["publication_date"].dt.date.value_counts()

        daily_counts_sorted = daily_counts.sort_index()

        top_titles = df["title"].value_counts().head(10)

        top_locations = df["location"].value_counts().head(10)

        return {
            "Top Job Titles": top_titles,
            "Top Locations": top_locations,
            "Job Postings per Day": daily_counts_sorted
        }

    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return None
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return {
            "Top Job Titles": pd.Series(dtype=	float64	),
            "Top Locations": pd.Series(dtype=	float64	),
            "Job Postings per Day": pd.Series(dtype=	float64	)
        }

