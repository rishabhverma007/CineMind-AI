import pandas as pd
import plotly.express as px


def charts(movies):
    data = pd.DataFrame(movies)
    if data.empty: return []
    rating = px.histogram(data, x="vote_average", nbins=10, title="Rating distribution", color_discrete_sequence=["#E50914"])
    popularity = px.bar(data.nlargest(10, "popularity"), x="title", y="popularity", title="Popularity pulse", color="vote_average", color_continuous_scale=["#7C3AED", "#06B6D4"])
    for fig in (rating, popularity):
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=45,b=10), font=dict(family="Inter"))
    return rating, popularity
