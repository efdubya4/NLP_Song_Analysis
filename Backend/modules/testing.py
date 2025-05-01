from lyric_analysis import LyricAnalyzer
import pandas as pd

# Sample lyrics (replace with your actual lyrics)
sample_lyrics = """
Frankie, didn't I tell you, you've got the world
In the palm of your hand
Frankie, didn't I tell you they're running
At your command
You know the tricks
As if they're your invention
It wasn't your intention
Frankie, to fall in the trap you made
Ohh, it's a crying shame, hmm
You left a trail of destruction
Heartbreaker you know now
They really did care 'cause it's your first affair
Frankie, didn't I tell you that the lion
Would come in for the kill
Frankie, didn't I say he had power
Over your sweet skill
So where is the laughter
You spat right in their faces
Didn't I tell you Frankie
That you might run out of races
Ohh, it's a crying shame, hmm
You couldn't win the game
Heartbreaker this time, this time
It's your first affair
Frankie, Frankie's first affair
It's your turn to cry, heartbreaker
Frankie, Frankie's first affair
It's your turn to cry
It's a crying shame
Heartbreaker
You know now they really did care
'Cause it's your first affair
Frankie, Frankie's first affair
Frankie, Frankie's first affair
It's your turn to cry, it's your turn to cry
It's your turn to cry, it's your turn to cry
Don't you realize they really, really, really did care (ah, ah)
The parties over, now you discover, it's your turn to cry (ah, ah)
And don't you realize (ah)
Ooh, it's the toughest thing, yes it is, yes it is (ah, ah)
The party's over, it's your turn to cry (ah, ah)
Ah (para-do-do-do) ah (para-do-do-do)
Ah, ah (hmm)
Ah (para-do-do-do) ah (para-do-do-do)
It's your turn to cry
"""

# Create a DataFrame with your lyrics
data = {'lyrics': [sample_lyrics]}
df = pd.DataFrame(data)

# Initialize the analyzer
analyzer = LyricAnalyzer()

# Add analysis features
df_with_analysis = analyzer.add_analysis_features(df)

# Display the sentiment results
print("Sentiment Analysis Results:")
print(f"Compound Sentiment: {df_with_analysis['sentiment_compound'][0]:.2f}")
print(f"Positive Sentiment: {df_with_analysis['sentiment_positive'][0]:.2f}")
print(f"Negative Sentiment: {df_with_analysis['sentiment_negative'][0]:.2f}")
print(f"TextBlob Polarity: {df_with_analysis['textblob_polarity'][0]:.2f}")
print(f"TextBlob Subjectivity: {df_with_analysis['textblob_subjectivity'][0]:.2f}")

# Display detected themes
print("\nDetected Themes:")
for theme in analyzer.theme_keywords:
    if df_with_analysis[f'theme_{theme}'][0]:
        print(f"- {theme.capitalize()}")