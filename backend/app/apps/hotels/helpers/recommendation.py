import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from django.conf import settings
from app import celery_app
from ..models import Hotel


def generate_score():
    """
    Generate the score for each hotel based on the IMDB algorithm
    """
    df_ = pd.DataFrame(list(Hotel.objects.all().values()))
    # Calculate C
    C = df_['star_rating'].mean()

    # The average rating of a hotel in Nairobi is around 3,2, on a scale of 5.

    # Next, let's calculate the number of votes, m, received by a hotel in the 55th percentile.
    # The pandas library makes this task extremely trivial using the .quantile() method of a pandas Series:
    m = df_['star_rating'].quantile(0.55)

    # we can filter the hotels that qualify for the chart, based on their vote counts:

    # Filter out all qualified movies into a new DataFrame
    qualified_hotels = df_.copy().loc[df_['star_rating'] >= m]

    def weighted_rating(x, m=m, C=C):
        """
        Function that computes the weighted rating of each hotel
        """
        v = x['total_reviews']
        R = x['star_rating']
        # Calculation based on the formula
        return (v/(v+m) * R) + (m/(m+v) * C)

    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    qualified_hotels['score'] = qualified_hotels.apply(weighted_rating, axis=1)

    df_to_db = qualified_hotels[['id', 'score']]
    return df_to_db

@celery_app.task(name="generate-recommendation")
def persist_to_db():
    """
    save the score to the database
    """
    engine = create_engine(settings.DB_CONN_STRING)
    df_to_db = generate_score()
    for i in range(1, len(df_to_db)+1):
        entry = df_to_db.iloc[i-1:i]
        score = entry['score'].values[0]
        id = entry['id'].values[0]
        update_sql = f"""UPDATE hotels_hotel SET score = '{score}' WHERE id = '{id}'"""
        with engine.begin() as conn:     # TRANSACTION
            conn.execute(update_sql)
