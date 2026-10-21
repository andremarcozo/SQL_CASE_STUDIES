
# --Q1 Identify matches played between two specific teams (e.g., India and South Africa) in 2024 and their results.
query_1 = """
SELECT Team1, Team2, MatchDate, Winner
FROM curso.dbo.T20I
WHERE Team1 IN ('India', 'South Africa')
  AND Team2 IN ('India', 'South Africa')
  AND YEAR(MatchDate) = 2024;
"""  



# --Q2 Find the team with the highest number of wins in 2024 and the total matches it won.

query_2 = """
SELECT top 1 Winner, COUNT(*) AS Wins_Count
FROM curso.dbo.T20I
GROUP BY Winner
order by Wins_Count DESC;
"""





# --Q3 Rank the teams based on the total number of wins in 2024.

query_3 = """
SELECT Winner, rank() over(order by Wins_Count DESC) as Winners_Rank, Wins_count
FROM(
SELECT Winner, COUNT(*) AS Wins_Count
FROM curso.dbo.T20I
GROUP BY Winner) as t;
"""




# --Q4 Which team had the highest average winning margin (in runs), and what was the average margin?

query_4 = """
SELECT top 1 Winner,
     AVG(CAST(REPLACE(REPLACE(Margin, ' runs', ''), ' run', '') AS INT)) AS Avg_Margin_Runs
FROM curso.dbo.T20I
WHERE Margin LIKE '%run%'
GROUP BY Winner
ORDER BY Avg_Margin_Runs DESC;
"""


# --Q4.1 Which team had the highest average winning margin (in wickets), and what was the average margin?
query_4_1 = """
SELECT top 1 Winner,
     AVG(CAST(REPLACE(REPLACE(Margin, ' wickets', ''), ' wicket', '') AS INT)) AS Avg_Margin_wicket
FROM curso.dbo.T20I
WHERE Margin LIKE '%wicket%'
GROUP BY Winner
ORDER BY Avg_Margin_wicket DESC;
"""




# --Q5 List all matches where the winning margin was greater than the average margin across all matches.
query_5 = """
WITH avg_win as (
SELECT *, AVG(CAST(REPLACE(REPLACE(REPLACE(REPLACE(Margin, ' wickets', ''), ' wicket', ''), 'runs', ''), 'run', '') AS INT)) OVER () AS winning_med
FROM curso.dbo.T20I
)
SELECT Team1, Team2, Winner, Margin, winning_med
FROM avg_win
WHERE CAST(REPLACE(REPLACE(REPLACE(REPLACE(Margin, ' wickets', ''), ' wicket', ''), 'runs', ''), 'run', '') AS INT) > winning_med;
"""




# --Q6 Find the team with the most wins when chasing a target (wins by wickets)
query_6 = """
WITH CTE AS(
SELECT *,
CASE 
	WHEN Margin LIKE '%wicket%' THEN 'Wicket_win'
	ELSE 'Run_win'
END as Win_Type
FROM curso.dbo.T20I
)
SELECT TOP 1 Winner, COUNT(Win_Type) AS Wicket_win_count
FROM CTE
WHERE Win_Type = 'Wicket_win'
GROUP BY Winner
ORDER BY Wicket_win_count DESC;
"""




# --Q7 Head-to-head record between two selected teams (e.g., England vs Australia).
QUERY_7 = """
SELECT *
FROM curso.dbo.T20I
WHERE Team1 IN ('England', 'Australia')
  AND Team2 IN ('England', 'Australia');
"""



# --Q8 Identify the month in 2024 with the highest number of T20I matches played.
Query_8 = """
SELECT MONTH(MatchDate) AS Match_Month ,COUNT(MONTH(MatchDate)) AS Count_Match_Month
FROM curso.dbo.T20I
WHERE YEAR(MatchDate) = 2024
GROUP BY MONTH(MatchDate)
"""


# --Q9 For each team, find how many matches they played in 2024 and their win percentage.

query_9 = """
WITH matches_played_as_team1 as (
select Team1, count(*) as count_matches_t1
FROM curso.dbo.T20I
group by Team1 
),
matches_played_as_team2 as (
select Team2, count(*) as count_matches_t2
FROM curso.dbo.T20I
group by Team2
),
matches_won as (
select Winner , count(*) as count_matches_won
FROM curso.dbo.T20I
group by Winner 
),
total_matches as (
SELECT 
    COALESCE(t1.Team1, t2.Team2) AS Team,
    ISNULL(t1.count_matches_t1, 0) + ISNULL(t2.count_matches_t2, 0) AS TotalMatchesPlayed
FROM matches_played_as_team1 t1
FULL OUTER JOIN matches_played_as_team2 t2 
    ON t1.Team1 = t2.Team2
)
SELECT 
    tm.Team,
    tm.TotalMatchesPlayed,
    ISNULL(mw.count_matches_won, 0) AS MatchesWon,
    ROUND((ISNULL(mw.count_matches_won, 0) * 100.0) / tm.TotalMatchesPlayed, 2) AS WinPercentage
FROM total_matches tm
LEFT JOIN matches_won mw
    ON tm.Team = mw.Winner
ORDER BY WinPercentage DESC;
"""



# --Q10 Identify the most successful team at each ground (team with most wins per ground).

