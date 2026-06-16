from groq import Groq
import json


# ---------------------------------------------------------
# Data Summary Helper
# ---------------------------------------------------------
def summarize_df(df):
    return {
        "columns": list(df.columns),
        "rows": len(df),
        "sample": df.head(5).to_dict(orient="records"),
        "stats": df.describe(include="all").to_dict()
    }


# ---------------------------------------------------------
# AI Recommendations Helper
# ---------------------------------------------------------
def generate_recommendations(jobs_df, employees_df, monthly_df, api_key):
    client = Groq(api_key=api_key)

    jobs_summary = summarize_df(jobs_df)
    employees_summary = summarize_df(employees_df)
    monthly_summary = summarize_df(monthly_df)

    # ---------------------------------------------------------
    # AI Prompt which can be changed
    # ---------------------------------------------------------
    prompt = f"""
    You are an expert business analyst.

    Here are summarized datasets in JSON format:

    Jobs Summary:
    {json.dumps(jobs_summary, indent=2)}

    Employees Summary:
    {json.dumps(employees_summary, indent=2)}

    Monthly Summary:
    {json.dumps(monthly_summary, indent=2)}

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
