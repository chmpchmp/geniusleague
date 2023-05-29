import pandas
import math
import matplotlib.image
import matplotlib.pyplot


XY_BOUNDS = [[-1735, 250], [-2024, 398], [-2806, 742], [-2472, 1233], [-1565, 580]]
Z_LOWER_BOUND = 285
Z_UPPER_BOUND = 421
MAP_IMAGE = 'de_overpass_radar.jpeg'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.slope = (second.y - first.y) / (second.x - first.x)
        self.y_intercept = second.y - second.x * self.slope


class Polygon:
    def __init__(self, points):
        self.points = self._convert_points(points)
        self.lines = self._create_lines(self.points)

    def _convert_points(self, points):
        return [Point(p[0], p[1]) for p in points]
    
    def _create_lines(self, points):
        return [Line(points[i], points[(i+1) % len(points)]) for i in range(len(points))]
    
    def in_region(self, point):
        cross_count = 0
        for line in self.lines:
            value = self._above_line(line, point)
            # return True immediately if the point is directly on the line
            if value == -1:
                return True
            # increment for every time the point with a line extending downwards passes a border of the polygon
            cross_count += value

        return cross_count % 2 == 1 # if the line crosses the polygon's borders an odd number of times then the point is in the polygon

    def _above_line(self, line, point):
        # return -1 if the point is directly on the line
        if math.isclose(point.y, line.slope * point.x + line.y_intercept):
            return -1
        
        x_value = point.x
        
        # shift the point slightly to the right if the x value is at the intersection of two lines
        if (point.x == line.first.x or point.x == line.second.x):
            x_value += 0.0001

        # return 0 if x is not in the domain (exclusive) OR the y value is below the line
        # return 1 if x is in the domain (exclusive) AND the y value is above the line
        if min(line.first.x, line.second.x) < x_value < max(line.first.x, line.second.x):
            if point.y > line.slope * x_value + line.y_intercept:
                return 1
        return 0


class ProcessGameState:
    def __init__(self, path):
        self.data = self._open_file(path)
        
    def _open_file(self, path):
        return pandas.read_parquet(path, engine = 'pyarrow')
    
    def _check_in_boundary(self):
        print('Running calculations...')
        print()

        polygon = Polygon(XY_BOUNDS)

        for index, row in self.data.iterrows():
            self.data.loc[index, 'in_boundary'] = self._in_boundary(polygon, row['x'], row['y'], row['z'])

    def _in_boundary(self, polygon, x, y, z):
        if z < Z_LOWER_BOUND or z > Z_UPPER_BOUND:
            return False
        return polygon.in_region(Point(x, y))
    
    def _select_rows(self, key, data_member):
        self.data = self.data[self.data[key] == data_member]
    
    def _delete_column(self, key):
        self.data = self.data.drop(key, axis=1)
    
    def _keep_columns(self, keys):
        self.data = self.data[keys]
    
    def _split_rounds(self):
        # returns a list of dataframes split by rounds, assume there is no overtime
        return [self.data[self.data['round_num'] == round_number] for round_number in range(1, 31)]
    
    def _split_players(self, rounds):
        # reads in a list of dataframes by rounds, returns list of lists of dataframes split by player
        output = []
        for round in rounds:
            player_data = []
            for n in range(0, 10):
                dataframe = round[round['player'] == f'Player{n}']
                if not dataframe.empty:
                    player_data.append(dataframe)
            if player_data != []:
                output.append(player_data)
        return output
    
    def get_inventory(self):
        return self.data['inventory']
    
    def create_spreadsheet(self, file_name):
        print('Creating spreadsheet...')
        self.data.to_excel(f'{file_name}.xlsx')
        print('Spreadsheet created!')
    
    def question_a(self):
        # select Team2 on T side
        self._select_rows('team', 'Team2')
        self._select_rows('side', 'T')

        # select the players that are still alive
        self._select_rows('is_alive', True)

        # select the rows that have a player in the boundary
        self._check_in_boundary()
        self._select_rows('in_boundary', True)
        
        # abstract away unneeded columns
        self._keep_columns(['round_num', 'side', 'team', 'is_alive', 'bomb_planted', 'player', 'in_boundary'])

        print(self.data)
        print()

    def question_b(self):
        # select Team2 on T side
        self._select_rows('team', 'Team2')
        self._select_rows('side', 'T')

        # select the players that are stil alive
        self._select_rows('is_alive', True)

        # assume that the bomb has not been planted and the T's are entering the site to plant
        self._select_rows('bomb_planted', False)
        self._select_rows('area_name', 'BombsiteB')

        # split the dataframe by round number, assume there is no overtime
        rounds = self._split_rounds()

        # split each sub-dataframe by player
        rounds = self._split_players(rounds)

        # iterate through each round, then each player, taking the first round time 
        for round in rounds:
            player_entry_times = []
            rifle_smg_count = 0

            # iterate through each player in the round
            for player_data in round:
                round_number = player_data['round_num'].loc[player_data.index[0]]
                player_entry_times.append(player_data['clock_time'].loc[player_data.index[0]])

                # iterate through each item in the player's inventory

                # only consider the moment they enter BombsiteB as they could pickup the weapons at the site
                for item in player_data['inventory'].loc[player_data.index[0]]:
                    if item['weapon_class'] == 'Rifle' or item['weapon_class'] == 'SMG':
                        rifle_smg_count += 1

            # find the average of the player entry times
            seconds = []
            for time in player_entry_times:
                seconds.append(int(time.split(':')[0]) * 60 + int(time.split(':')[1]))
            average_seconds = sum(seconds) / len(seconds)
            average_time = f'{"{:02d}".format(int(average_seconds / 60))}:{"{:02d}".format(int(average_seconds % 60 + 0.5))}'

            if len(player_entry_times) == 1:
                print(f'Round {round_number}, {len(player_entry_times)} T entering')
            else:
                print(f'Round {round_number}, {len(player_entry_times)} T\'s entering')
            print(f'    Player entry times: {player_entry_times}')
            print(f'    Average player entry time: {average_time}')
            print(f'    SMG/Rifle count: {rifle_smg_count}')
            print()
    
    def question_c(self):
        # select Team2 on CT side
        self._select_rows('team', 'Team2')
        self._select_rows('side', 'CT')

        # select the players that are stil alive
        self._select_rows('is_alive', True)

        # assume that the bomb has not been planted and the CT's are waiting at the site
        self._select_rows('bomb_planted', False)
        self._select_rows('area_name', 'BombsiteB')
  
        # split the dataframe by round number, assume there is no overtime
        rounds = self._split_rounds()

        # split each sub-dataframe by player
        rounds = self._split_players(rounds)

        image_data = matplotlib.image.imread(MAP_IMAGE)
        matplotlib.pyplot.imshow(image_data)

        show_players = ['Player5',
                        'Player6',
                        'Player7',
                        'Player8',
                        'Player9',
                        ]
        
        colors = {'Player5': 'red',
                  'Player6': 'orange',
                  'Player7': 'green',
                  'Player8': 'blue',
                  'Player9': 'purple'
                  }

        # iterate through each round, then each player, taking the first round time 
        for round in rounds:
            color_index = 0
            for player_data in round:
                player = player_data['player'].loc[player_data.index[0]]
                if player in show_players:
                    for index, row in player_data.iterrows():
                        x_value = 0.19 * row['x'] + 935
                        y_value = -0.19 * row['y'] + 340
                        matplotlib.pyplot.plot(x_value, y_value, marker = '.', color = colors[player])

        matplotlib.pyplot.show()


if __name__ == '__main__':
    ProcessGameState('game_state_frame_data.parquet').question_a()
    ProcessGameState('game_state_frame_data.parquet').question_b()
    ProcessGameState('game_state_frame_data.parquet').question_c()