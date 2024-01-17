# geniusleague

This was an assessment for Evil Geniuses' summer 2023 software engineering internship program application.

### Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?
To find the answer to this problem, I first had to simplify the table from the data that was given. I selected the rows of the table that had 'team' = 'Team2', 'side' = 'T', and 'is_alive' = True. Then, I added a column to the table called 'in_boundary' that is only true if the coordinates of the player of the row is within the constraints that were given. Next, I selected the rows of the table that had 'in_boundary' = True. After removing some unnecessary columns, the table looks like this:

![image](https://github.com/chmpchmp/geniusleague/assets/108765830/ce1cba85-12ca-4004-b2e1-7b0554afc70e)

The image shows that there were only two instances where a T on Team2 entered the light blue boundary, both in the same round. However, these instances were both after the bomb was planted so these players did not actually enter the bombsite through the region. Thus, it would be extremely unlikely for Team2 to enter BombsiteB from the light blue boundary.

### What is the average timer that Team2 on T (terrorist) side enters “BombsiteB” with least 2 rifles or SMGs?
Similar to the previous problem, I selected the rows of the table that had 'team' = 'Team2', 'side' = 'T', and 'is_alive' = True. In addition, I selected the rows with ‘bomb_planted’ = False and ‘area_name’ = ‘BombsiteB’, because we can assume that the act of entering a bombsite requires the bomb not to be planted. Then, I split the table by each round of the game, and each of those subtables by each player in the game. Next, I went through each round and found the first tick and its corresponding row when each player entered the bombsite to record the in-game time and their inventories. I then took the average entry time out of all the players for each round and the number of total rifles or SMGs they had.

![image](https://github.com/chmpchmp/geniusleague/assets/108765830/70fd2d52-b7ad-445f-aa2d-71dec85d5ae8)

Out of the six rounds Team2 on their T side entered BombsiteB, they only had at least two rifles or SMGs in only three of the rounds. The average entry time of the three rounds (01:36, 01:23, 01:17) is 01:25.

### Now that we’ve gathered data on Team2 T side, let's examine their CT (counter-terrorist) Side. Using the same data set, tell our coaching staff where you suspect them to be waiting inside “BombsiteB”
This time I selected the rows of the table that had 'team' = 'Team2', 'side' = 'CT', 'is_alive' = True, ‘bomb_planted’ = False, and ‘area_name’ = ‘BombsiteB’, making the assumption that in order for the CTs to wait for the Ts at a bombsite, the bomb cannot be planted. Again, I split the table by each round of the game, and each of those subtables by each player in the game. Then, I took every row’s coordinates and plotted it onto a map of de_overpass with this legend:

![image](https://github.com/chmpchmp/geniusleague/assets/108765830/8022e6bb-52d8-446e-842e-aec5bbc6049a)

The points plotted onto the minimap looks like this:

![image](https://github.com/chmpchmp/geniusleague/assets/108765830/958adbcb-c859-4d95-8e47-cfe9ac50b1bf)

There are a few takeaways from looking at this image. Player5 (red) and Player6 (orange) are the main players who play at BombsiteB, with Player7 (green) being there too, but not as frequently. Player8 (blue) and Player9 (purple) are hardly ever seen at BombsiteB, and we can assume that these two players do not ever wait at BombsiteB. Player7 almost always waits behind the pillar in the middle of the bombsite. With Player5 and Player6, there is a relatively high chance that at least one of them will be behind the geometry at the top of the bombsite. In addition, it seems that it is very unlikely for a player to be waiting where the bomb can be planted in the red region.

### Most of the time, our stakeholders (in this case, the CS:GO coaching staff) aren’t tech-savvy enough to run code themselves. Propose a solution to your product manager that could allow our coaching staff to request or acquire the output themselves and takes less than 1 weeks worth of work to implement.
I think that a simple interface, using something like tkinter, to select certain rows or columns of the data table could be used by the CS:GO coaching staff to acquire the output themselves and could be easily implemented within a week. For an extremely simple implementation, have a textbox that enables the user to choose a column by key and remove it and allow the user to enter a column and a value in the column into two textboxes to select the rows that are wanted in the table. Then, the user would click a button to show the final table. For a more complex implementation, show the whole table on the interface and allow the user to click columns to remove them directly or click values in a row to select all rows with the same value in that column. Additionally, the final table could be converted to an Excel spreadsheet for the coaches to easily read.
