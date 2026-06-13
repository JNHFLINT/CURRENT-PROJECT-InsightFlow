from groq import Groq

def summarize_df(df):
    return {
        "columns": list(df.columns),
        "rows": len(df),
        "sample": df.head(5).to_dict(orient="records"),
        "stats": df.describe(include="all").to_dict()
    }

def generate_recommendations(jobs_df, employees_df, monthly_df, api_key):
    client = Groq(api_key=api_key)

    jobs_summary = summarize_df(jobs_df)
    employees_summary = summarize_df(employees_df)
    monthly_summary = summarize_df(monthly_df)

    prompt = f"""
    You are an expert business analyst.

    Here are summarized datasets:

    Jobs Summary:
    {jobs_summary}

    Employees Summary:
    {employees_summary}

    Monthly Summary:
    {monthly_summary}

    Based on these summaries, provide:
    - Key insights
    - Trends
    - Risks
    - Recommended actions
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
