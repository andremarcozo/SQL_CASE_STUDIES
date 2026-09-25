# --Q1 Find the total spending on players for each team:
query_1 = """
select sum(Price_in_cr) as Total_Spending_per_team
, Team
from curso.dbo.IPLPlayers
group by Team;
"""



# --Q2 Find the top 3 highest-paid 'All-rounders' across all teams: 
query_2 = """
SELECT TOP 3 
    player,
    Price_in_cr
FROM curso.dbo.IPLPlayers
WHERE Role = 'All-rounder' 
ORDER BY Price_in_cr DESC;
"""

# --Q3 Find the highest-priced player in each team:
query_3 = """
WITH RankingEquipes AS (
    SELECT 
        Player,
        Team,
        Price_in_cr,
        RANK() OVER (PARTITION BY Team ORDER BY Price_in_cr DESC) AS rn
    FROM curso.dbo.IPLPlayers
)
SELECT 
    Player,
    Team,
    Price_in_cr
FROM RankingEquipes
WHERE rn = 1;
"""



# --Q4 Rank players by their price within each team and list the top 2 for every team:
query_4 = """
WITH RankingEquipes AS (
    SELECT 
        Player,
        Team,
        Price_in_cr,
        RANK() OVER (PARTITION BY Team ORDER BY Price_in_cr DESC) AS rn
    FROM curso.dbo.IPLPlayers
)
SELECT 
    Player,
    Team,
    Price_in_cr
FROM RankingEquipes
WHERE rn <= 2;
"""

# --Q5 Find the most expensive player from each team, along with the second-most expensive player's name and price:
query_5 = """
WITH DadosCompletos AS (
    SELECT 
        Team,
        Player AS Top_Player,
        Price_in_cr AS Top_Price,
        LEAD(Player) OVER (PARTITION BY Team ORDER BY Price_in_cr DESC) AS Second_Player,
        LEAD(Price_in_cr) OVER (PARTITION BY Team ORDER BY Price_in_cr DESC) AS Second_Price,
        ROW_NUMBER() OVER (PARTITION BY Team ORDER BY Price_in_cr DESC) AS rn
    FROM curso.dbo.IPLPlayers
)
SELECT 
    Team,
    Top_Player,
    Top_Price,
    Second_Player,
    Second_Price
FROM DadosCompletos
WHERE rn = 1;
"""



# --Q6 Calculate the percentage contribution of each player's price to their team's total spending
query_6 = """
WITH total_spend_per_team AS (
SELECT Team,
SUM(Price_in_cr) as Total_per_team
FROM curso.dbo.IPLPlayers
GROUP BY Team
)
SELECT b.Player,
b.Team,
round((b.Price_in_cr/a.Total_per_team)*100.0,2) AS  percentage_spent_player_by_team
FROM total_spend_per_team a
join curso.dbo.IPLPlayers b
on a.Team = b.Team 
order by percentage_spent_player_by_team DESC;
"""



# --Q7 Classify players as 'High', 'Medium', or 'Low' priced based on the following rules:
# --High: Price > ₹15 crore
# --Medium: Price between ₹5 crore and ₹15 crore
# --Low: Price < ₹5 crore
# --and find out the number of players in each bracket

query_7 = """
WITH Classify_price as (
SELECT Player,
Price_in_cr,
CASE 
	WHEN Price_in_cr > 15 THEN 'High'
	WHEN Price_in_cr BETWEEN 5 AND 15 THEN 'Medium'
	WHEN Price_in_cr < 5 THEN 'Low'
END as Player_price_range
FROM curso.dbo.IPLPlayers)
SELECT a.Player_price_range,
count(*) AS Players_in_each_bracket
FROM Classify_price a
join curso.dbo.IPLPlayers b
on a.player = b.Player 
GROUP BY  a.Player_price_range
ORDER BY Players_in_each_bracket DESC;
"""



# --Q8 Find the average price of Indian players and compare it with overseas players using a subquery:

query_8 = """
SELECT AVG(price_in_cr) as Avg_Price,
Player_Origin
FROM (
SELECT price_in_cr,
	CASE WHEN [type] LIKE 'India%' THEN 'Indian'
	     ELSE 'Overseas'
	     end as Player_Origin
	FROM curso.dbo.IPLPlayers   
	) AS origin
GROUP BY Player_origin;
"""





# --Q9 Identify players who earn more than the average price of their team:
query_9 = """
WITH avg_price_per_team AS(
SELECT AVG(Price_in_cr) AS Avg_Price,
Team
FROM curso.dbo.IPLPlayers
GROUP BY Team
)
SELECT a.Player,
a.Price_in_cr,
b.Avg_Price,
a.Team,
CASE WHEN a.Price_in_cr > b.Avg_Price THEN 'Earn more than average'
	 WHEN a.Price_in_cr = b.Avg_Price THEN 'Earn the avarage'
	 Else 'Earn less than avarage'
	 END AS Comparative_earnings
FROM curso.dbo.IPLPlayers a
JOIN avg_price_per_team b
on a.Team = b.Team 
ORDER BY Player DESC;
"""


# --Q10 For each role, find the most expensive player and their price using a correlated subquery


					







