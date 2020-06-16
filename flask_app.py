from flask import Flask, render_template, request, url_for
import sqlalchemy
import pandas as pd
# import pymysql
from wtforms import Form, validators, StringField
#from plotly import plot
import matplotlib.pyplot as plt
import numpy as np
import plotly
import base64
import io
import json


# App config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '3306'
app.config['MYSQL_PASSWORD'] = 'Msqli1m.'
app.config['MYSQL_DB'] = 'fifa20'


class teamForm(Form):
    team = StringField('Team', [validators.Length(min=6, max=35)],[validators.data_required()])


class playerForm(Form):
    player = StringField('Player', [validators.Length(min=6, max=35)],[validators.data_required()])


# creating the app
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response





@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('/index.html')


# creating the player page
@app.route('/players.html', methods=['GET', 'POST'])
def players():
    if request.method == "POST":
        players = request.form.get("player") #cntr+/
        engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:Msqli1m.@localhost:3306/fifa20')
        # SQL Query to get informataion about the player
        dbConnection = engine.connect()
        try:
            # Getting the player name and their position
            SQL_Querypa = pd.read_sql_query(
                '''SELECT players.short_name,players.long_name,players.team_position 
                FROM players
                where players.short_name = '''+ '\''+str(players)+'\'' +'''
                  or players.long_name= '''+ '\''+ str(players)+'\'' +''' ''', con=dbConnection)
            dfpa = pd.DataFrame(SQL_Querypa)
            #Checking if player exist in the db
        except IndexError as e:
            return ('Player not in database or incorrect spelling please check and try again.Please check your spelling or sofifa website')
        else:
            goalk=['GK']
            defenders=['CB','LB','RB','RWB','LWB']
            midfielders=['CM','CDM','CAM']
            attackers=['LM','LW','RM','RW','CF','ST']
            playerpos=(list(dfpa['team_position']))
            gk=['M. Ter Stegen','J. Oblak','Alisson','Ederson','M. Neuer']
            de=['V. van Dijk','K. Koulibaly','R. Varane','T. Alexander-Arnold','A. Robertson']
            mi=['P. Pogba','T. Kroos','N. Kante','K. De Bruyne','L. Modric','Casemiro ','C. Eriksen']
            at=['Neymar Jr','Harry Kane','Luis Alberto Suarez Diaz','C. Ronaldo','K. Benzema','R. Lewandowski','K. Mbappe','M. Salah','L. Messi','S. Mane']
            gkp = []
            dep = []
            midp = []
            attp = []
            plot_urlgp=[]
            plot_urldp = []
            plot_urlmp = []
            plot_urlap =[]
            if len(set(playerpos).intersection(goalk)) == 1:
                if str(players) not in gk:
                    gkp.append(str(players))
                    finalgk = gkp + gk
                for fg in finalgk:
                    SQL_Query = pd.read_sql_query(
                        '''SELECT players.short_name, players.age,players.club,
                          players.overall,players.potential,players.height_cm,players.weight_kg,
                            gk.goalkeeping_diving,gk.goalkeeping_reflexes,gk.goalkeeping_positioning,gk.goalkeeping_handling,
                             gk.goalkeeping_kicking,teams.League,players.player_url
                             FROM players 
                             LEFT JOIN gk on gk.sofifa_id = players.sofifa_id
                             LEFT JOIN teams on teams.Teams = players.club
                             where players.short_name=  ''' + '\'' + fg + '\'' + ''' or players.long_name=  ''' + '\'' + fg + '\'' + '''
                           ''', con=dbConnection)
                    df1 = pd.DataFrame(SQL_Query)

                    for i in range(0, len(df1)):
                        df = pd.DataFrame({
                            'Col A': ['Diving', 'Reflexes', 'Positioning', 'Handling', 'Kicking'],
                            'Col B': df1[
                                ['goalkeeping_diving', 'goalkeeping_reflexes', 'goalkeeping_positioning',
                                 'goalkeeping_handling',
                                 'goalkeeping_kicking']].iloc[i]})

                        fig = plt.figure()
                        img = io.BytesIO()
                        ax = fig.add_subplot(111, projection="polar")

                        # theta has 5 different angles, and the first one repeated
                        theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                        # values has the 5 values from 'Col B', with the first element repeated
                        values = df['Col B'].values
                        values = np.append(values, values[0])

                        # draw the polygon and the mark the points for each angle/value combination
                        l1, = ax.plot(theta, values, color="blue", marker="o", label="Name of Col B")
                        plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                        ax.tick_params(pad=10)  # to increase the distance of the labels to the plot
                        # fill the area of the polygon with green and some transparency
                        ax.fill(theta, values, 'blue', alpha=0.1)
                        plt.title(df1['short_name'][i])
                        fig.savefig(img, format='png')
                        img.seek(0)
                        plot_urlgp.append(base64.b64encode(img.getvalue()).decode())
            else:
                    if len(set(playerpos).intersection(defenders)) == 1:
                        if players not in de:
                            dep.append(players)
                            finalde = dep + de
                        for fe in finalde:
                            SQL_Query = pd.read_sql_query(
                                '''SELECT players.short_name, players.age,players.club,
                                    players.overall,players.potential,players.height_cm,players.weight_kg,
                                    attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
                                defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
                                attack.attacking_short_passing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision,teams.League
                                    ,players.player_url,players.team_position
                            FROM players 
                            LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                            LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                            LEFT JOIN power on power.sofifa_id = players.sofifa_id
                            LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                            LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                            LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                            LEFT JOIN teams on teams.Teams = players.club
                            where players.short_name=  ''' + '\'' + fe + '\'' + ''' or players.long_name=  ''' + '\'' + fe + '\'' + '''
                                               ''', con=dbConnection)
                            df2 = pd.DataFrame(SQL_Query)
                            for i in range(0, len(df2)):
                                df = pd.DataFrame({
                                    'Col A': ['Sprint_speed', 'Strength', 'Heading_accuracy', 'Aggression'
                                        , 'Vision', 'Composure', 'Reactions',
                                              'Short_passing', 'Long_passing', 'Crossing', 'Interceptions', 'Marking',
                                              'Slide_tackle', 'Stand_tackle'],
                                    'Col B': df2
                                        [['movement_sprint_speed', 'power_strength', 'attacking_heading_accuracy'
                                                , 'mentality_aggression', 'mentality_vision'
                                                , 'mentality_composure', 'movement_reactions', 'attacking_short_passing',
                                          'skill_long_passing', 'attacking_crossing', 'mentality_interceptions',
                                          'defending_marking'
                                                , 'defending_standing_tackle', 'defending_sliding_tackle']].iloc[i]})
                                fig = plt.figure()
                                img = io.BytesIO()
                                ax = fig.add_subplot(111, projection="polar")

                                # theta has 5 different angles, and the first one repeated
                                theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                                # values has the 5 values from 'Col B', with the first element repeated
                                values = df['Col B'].values
                                values = np.append(values, values[0])
                                # draw the polygon and the mark the points for each angle/value combination
                                l1, = ax.plot(theta, values, color="green", marker="o", label="Name of Col B")
                                plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                                ax.tick_params(pad=10)  # to increase the distance of the labels to the plot
                                # fill the area of the polygon with green and some transparency
                                ax.fill(theta, values, 'green', alpha=0.1)
                                plt.title(df2['short_name'][i])
                                fig.savefig(img, format='png')
                                img.seek(0)
                                plot_urldp.append(base64.b64encode(img.getvalue()).decode())
                    else:
                        if len(set(playerpos).intersection(midfielders)) == 1:

                            if str(players) not in mi:
                                midp.append(str(players))
                            finalmid = midp + mi
                            for fm in finalmid:
                                SQL_Query = pd.read_sql_query(
                                    '''SELECT players.short_name, players.age,players.club,players.team_position,players.player_url,
                                        players.overall,players.potential,players.height_cm,players.weight_kg,
                                        attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
                                    defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
                                    attack.attacking_finishing,attack.attacking_short_passing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision,teams.League
                                    FROM players 
                                    LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                                    LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                                    LEFT JOIN power on power.sofifa_id = players.sofifa_id
                                    LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                                    LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                                    LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                                    LEFT JOIN teams on teams.Teams = players.club
                                    where players.short_name=  ''' + '\'' + fm + '\'' + ''' or players.long_name=  ''' + '\'' + fm + '\'' + '''
                                                                       ''', con=dbConnection)
                                df3 = pd.DataFrame(SQL_Query)
                                # Creating the radar chart for each player in the selected team for the data analysis

                                for i in range(0, len(df3)):
                                    df = pd.DataFrame({
                                        'Col A': ['Heading_accuracy', 'Interceptions', 'Marking', 'Slide_tackle',
                                                  'Stand_tackle',
                                                  'Aggression', 'Composure', 'Strength', 'Reactions',
                                                  'Short_passing', 'Long_passing', 'Crossing', 'Sprint_speed', 'Vision'],
                                        'Col B':
                                            df3[['attacking_heading_accuracy', 'mentality_interceptions', 'defending_marking'
                                                , 'defending_standing_tackle',
                                                 'defending_sliding_tackle', 'mentality_aggression', 'mentality_composure',
                                                 'power_strength',
                                                 'movement_reactions', 'attacking_short_passing', 'skill_long_passing',
                                                 'attacking_crossing',
                                                 'movement_sprint_speed', 'mentality_vision']].iloc[i]})

                                    fig = plt.figure()
                                    img = io.BytesIO()
                                    ax = fig.add_subplot(111, projection="polar")
                                    # theta has 5 different angles, and the first one repeated
                                    theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                                    # values has the 5 values from 'Col B', with the first element repeated
                                    values = df['Col B'].values
                                    values = np.append(values, values[0])

                                    # draw the polygon and the mark the points for each angle/value combination
                                    l1, = ax.plot(theta, values, color="grey", marker="o", label="Name of Col B")
                                    plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                                    ax.tick_params(pad=10)  # to increase the distance of the labels to the plot
                                    # fill the area of the polygon with green and some transparency
                                    ax.fill(theta, values, 'grey', alpha=0.1)
                                    plt.title(df3['short_name'][i])
                                    fig.savefig(img, format='png')
                                    img.seek(0)

                                    plot_urlmp.append(base64.b64encode(img.getvalue()).decode())
                        else:
                            if len(set(playerpos).intersection(attackers)) == 1:
                                if players not in at:
                                    attp.append(players)
                                    finalat=attp+ at
                                for fa in finalat:
                                    SQL_Query = pd.read_sql_query(
                                        '''SELECT players.short_name, players.age,players.club,players.team_position,players.player_url,
                                    players.overall,players.potential,players.height_cm,players.weight_kg,
                                    attack.attacking_heading_accuracy,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
                                    attack.attacking_finishing,movement.movement_sprint_speed,mentality.mentality_penalties,movement_agility,movement_balance,
                                    mentality.mentality_positioning,attack.attacking_volleys,teams.League
                                    FROM players 
                                    LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                                    LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                                    LEFT JOIN power on power.sofifa_id = players.sofifa_id
                                    LEFT JOIN movement on movement.sofifa_id = players.sofifa_id                                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                                    LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                                    LEFT JOIN teams on teams.Teams = players.club
                                    where players.short_name=  ''' + '\'' + fa + '\'' + ''' or players.long_name=  '''
                                        + '\'' + fa + '\'' + '''''', con=dbConnection)
                                    df4 = pd.DataFrame(SQL_Query)
                                # Creating the radar chart for each player in the selected team for the data analysis
                                    for i in range(0, len(df4)):
                                            df = pd.DataFrame({
                                                'Col A': ['Heading_accuracy', 'Aggression', 'Composure', 'Strength'
                                                    , 'Reactions', 'Sprint_speed', 'Finishing', 'Penalities'],
                                                'Col B': df4
                                                [['attacking_heading_accuracy', 'mentality_aggression', 'mentality_composure', 'power_strength',
                                                  'movement_reactions', 'movement_sprint_speed', 'attacking_finishing',
                                                  'mentality_penalties']].iloc[i]})

                                            fig = plt.figure()
                                            img = io.BytesIO()
                                            ax = fig.add_subplot(111, projection="polar")

                                            # theta has 5 different angles, and the first one repeated
                                            theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                                            # values has the 5 values from 'Col B', with the first element repeated
                                            values = df['Col B'].values
                                            values = np.append(values, values[0])

                                            # draw the polygon and the mark the points for each angle/value combination
                                            l1, = ax.plot(theta, values, color="purple", marker="o", label="Name of Col B")
                                            plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                                            ax.tick_params(pad=10)  # to increase the distance of the labels to the plot
                                            # fill the area of the polygon with green and some transparency
                                            ax.fill(theta, values, 'purple', alpha=0.1)
                                            plt.title(df4['short_name'][i])
                                            fig.savefig(img, format='png')
                                            img.seek(0)

                                            plot_urlap.append(base64.b64encode(img.getvalue()).decode())
                            else:
                                return ('Player not in database or incorrect spelling please check and try again.Please check your spelling or sofifa website')
        return render_template('/playersr.html',plot_urlgp=plot_urlgp,plot_urldp=plot_urldp
                               ,plot_urlmp=plot_urlmp,plot_urlap=plot_urlap,players=players)
    else:
        return render_template('/players.html')

@app.route('/teamsda.html', methods=['GET', 'POST'])
def teamsda():
    if request.method == "POST":
        teams = request.form.get("team")
        engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:Msqli1m.@localhost:3306/fifa20')
        # SQL Query to get goalkeeper information for player who play for the selected team
        dbConnection = engine.connect()
        try:
            #Getting the team and information on the league they play in
            SQL_Queryl = pd.read_sql_query(
                '''SELECT teams.League
                FROM players
                LEFT JOIN teams on teams.Teams = players.club
                where  teams.Teams =  ''' + '\'' + str(teams) + '\'' + '''
                ''', con=dbConnection)
            dfl = pd.DataFrame(SQL_Queryl)
            league = str(dfl['League'][1])
            SQL_Queryws = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,players.value_eur,players.wage_eur,teams.League
                FROM players
                LEFT JOIN teams on teams.Teams = players.club
                where  teams.League =  ''' + '\'' + league + '\'' + '''
                ''', con=dbConnection)
            dfws = pd.DataFrame(SQL_Queryws)
            clubname = [teams]
            dfws['club'] = ['<b>' + x + '</b>' if x in clubname else x for x in dfws.club]
            height = dfws.groupby('club')['height_cm'].mean().reset_index()
            height = height.sort_values('height_cm')
            weight = dfws.groupby('club')['weight_kg'].mean().reset_index()
            weight = weight.sort_values('weight_kg')
            playerve = dfws.groupby('club')['value_eur'].mean().reset_index()
            playerve = playerve.sort_values('value_eur')
            playerwe = dfws.groupby('club')['wage_eur'].mean().reset_index()
            playerwe = playerwe.sort_values('wage_eur')
            #query for gk in the sleected team
            SQL_Query = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,
            gk.goalkeeping_diving,gk.goalkeeping_reflexes,gk.goalkeeping_positioning,gk.goalkeeping_handling,
            gk.goalkeeping_kicking,teams.League
                FROM players 
                LEFT JOIN gk on gk.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where players.team_position='GK' and teams.Teams =  ''' + '\'' + teams + '\'' + '''
                ''', con=dbConnection)
            dfs = pd.DataFrame(SQL_Query)
            league = str(dfs.League[0])
            team = str(dfs.club[0])
            keepers = list(dfs.short_name)
            #Query for goalkeeping in the same league
            SQL_Querygk = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,
            gk.goalkeeping_diving,gk.goalkeeping_reflexes,gk.goalkeeping_positioning,gk.goalkeeping_handling,
            gk.goalkeeping_kicking,teams.League_ID
                FROM players 
                LEFT JOIN gk on gk.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where players.team_position='GK' and teams.League =  ''' + '\'' + league + '\'' + '''
                ''', con=dbConnection)
            # Distinguishing the selected team from other teams
            dfgk = pd.DataFrame(SQL_Querygk)
            dfgk['short_name'] = ['<b>' + x + '</b>' if x in keepers else x for x in dfgk.short_name]
            dfgk['color'] = [x for x in dfgk['short_name']]
            dfgk['color'] = dfgk.loc[dfgk['club'] != team] == False
            dfgk['color'] = dfgk.color.replace(False, 'blue')
            dfgk['color'] = dfgk.color.fillna(0)
            dfgk['color'] = dfgk.color.replace(0, 'red')
            #Defenders
            SQL_Queryde = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,
                attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
            defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_short_passing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision,teams.League
                FROM players 
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('CB' , 'LB' , 'RB' , 'RWB' , 'LWB'))
                 and teams.Teams =  ''' + '\'' + teams + '\'' + '''
                ''', con=dbConnection)
            dfde = pd.DataFrame(SQL_Queryde)
            league = str(dfde.League[0])
            team = str(dfde.club[0])
            defenders = list(dfde.short_name)
            # SQL Query to get defenders (cb,rb,lwb,rwb,lb) information for player who play for the selected team and teams in the same division
            SQL_Querydea = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,players.overall,players.potential,
             attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
            defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_short_passing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision
                ,power.power_jumping
                FROM players 
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('CB' , 'LB' , 'RB' , 'RWB' , 'LWB')) and teams.League =  ''' + '\'' + league + '\'' + '''
                ''', con=dbConnection)
            # Creating the graph for the data analysis
            dfdea = pd.DataFrame(SQL_Querydea)
            dfdea['short_name'] = ['<b>' + x + '</b>' if x in defenders else x for x in dfdea.short_name]
            dfdea['color'] = [x for x in dfdea['short_name']]
            dfdea['color'] = dfdea.loc[dfdea['club'] != team] == False
            dfdea['color'] = dfdea.color.replace(False, 'green')
            dfdea['color'] = dfdea.color.fillna(0)
            dfdea['color'] = dfdea.color.replace(0, 'red')
            #Midfielders
            SQL_Querymid = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,
                attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
            defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_finishing,attack.attacking_short_passing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision,teams.League
                FROM players 
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('CAM','CDM','CM')) and teams.Teams =  ''' + '\'' + teams + '\'' + '''
                ''', con=dbConnection)
            dfmid = pd.DataFrame(SQL_Querymid)
            league = str(dfmid.League[0])
            team = str(dfmid.club[0])
            midfielders = list(dfmid.short_name)
            # SQL Query to get midfielders (CM,CAM,CDM) information for player who play for the selected team and teams in the same division
            SQL_Querymida = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
             attack.attacking_heading_accuracy,mentality.mentality_interceptions,defend.defending_marking,defend.defending_sliding_tackle,
            defend.defending_standing_tackle,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_short_passing,attack.attacking_finishing,skill.skill_long_passing,attack.attacking_crossing,movement.movement_sprint_speed,mentality.mentality_vision,
            power.power_long_shots,movement.movement_agility,movement.movement_balance,power.power_jumping,skill.skill_dribbling

                FROM players 
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('CM','CAM','CDM')) and teams.League =  ''' + '\'' + league + '\'' + '''
                ''', con=dbConnection)
            # Creating the graph for the data analysis
            dfmida = pd.DataFrame(SQL_Querymida)
            dfmida['short_name'] = ['<b>' + x + '</b>' if x in midfielders else x for x in dfmida.short_name]
            dfmida['color'] = [x for x in dfmida['short_name']]
            dfmida['color'] = dfmida.loc[dfmida['club'] != team] == False
            dfmida['color'] = dfmida.color.replace(False, 'grey')
            dfmida['color'] = dfmida.color.fillna(0)
            dfmida['color'] = dfmida.color.replace(0, 'red')
            #Attackers
            SQL_Queryatt = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
                players.overall,players.potential,players.height_cm,players.weight_kg,
                attack.attacking_heading_accuracy,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_finishing,movement.movement_sprint_speed,mentality.mentality_penalties,movement_agility,movement_balance,
            mentality.mentality_positioning,attack.attacking_volleys,teams.League
                FROM players 
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('LM','LW','RM','RW','CF','ST')) and teams.Teams =  ''' + '\'' + teams + '\'' + '''
                ''', con=dbConnection)
            dfatt = pd.DataFrame(SQL_Queryatt)
            league = str(dfatt.League[0])
            team = str(dfatt.club[0])
            attackers = list(dfatt.short_name)
            SQL_Queryatta = pd.read_sql_query(
                '''SELECT players.short_name, players.age,players.club,
            attack.attacking_heading_accuracy,mentality.mentality_aggression,mentality.mentality_composure,power.power_strength,movement.movement_reactions,
            attack.attacking_finishing,movement.movement_sprint_speed,mentality.mentality_penalties,movement_agility,movement_balance,skill.skill_dribbling,power.power_jumping
            ,mentality.mentality_positioning,attack.attacking_volleys,teams.League
                FROM players  
                LEFT JOIN defend on defend.sofifa_id = players.sofifa_id
                LEFT JOIN attack on attack.sofifa_id = players.sofifa_id
                LEFT JOIN power on power.sofifa_id = players.sofifa_id
                LEFT JOIN movement on movement.sofifa_id = players.sofifa_id
                LEFT JOIN mentality on  mentality.sofifa_id = players.sofifa_id
                LEFT JOIN skill on skill.sofifa_id = players.sofifa_id
                LEFT JOIN teams on teams.Teams = players.club
                where (players.team_position in ('LM','LW','RM','RW','CF','ST')) and teams.League =  ''' + '\'' + league + '\'' + '''
                ''', con=dbConnection)
            # Creating the graphs for the data analysis
            dfatta = pd.DataFrame(SQL_Queryatta)
            dfatta['short_name'] = ['<b>' + x + '</b>' if x in attackers else x for x in dfatta.short_name]
            dfatta['color'] = [x for x in dfatta['short_name']]
            dfatta['color'] = dfatta.loc[dfatta['club'] != team] == False
            dfatta['color'] = dfatta.color.replace(False, 'purple')
            dfatta['color'] = dfatta.color.fillna(0)
            dfatta['color'] = dfatta.color.replace(0, 'red')
            #Transfers
            SQL_Queryt = pd.read_sql_query(
                '''SELECT players.short_name,players.team_position,players.age,
                players.overall,players.potential,players.value_eur,players.wage_eur
                ,players.release_clause_eur,players.contract_valid_until,teams.attack,teams.midfield,
                teams.budget,teams.Dprestige,teams.Iprestige
                FROM players 
                LEFT JOIN teams on teams.Teams = players.club
                where teams.Teams =  ''' + '\'' + teams + '\'' + '''
                ''', con=dbConnection)
            dft = pd.DataFrame(SQL_Queryt)
            # age less than or equal to + overall equal to avg overall and potential greater than or equal to av potential
            # within team
            # print display(dft)
            defenders = ['CB', 'LB', 'RB', 'RWB', 'LWB']
            midfieldp = ['CM', 'CDM', 'CAM']
            attackers = ['LM', 'LW', 'RM', 'RW', 'CF', 'ST']
            gk = dft[dft['team_position'] == 'GK']
            defs = dft[dft['team_position'].isin(defenders)]
            mids = dft[dft['team_position'].isin(midfieldp)]
            atts = dft[dft['team_position'].isin(attackers)]

            tbud = str((dft.budget[0]))
            tdp = str(dft.Dprestige[0])
            tip = str(dft.Iprestige[0])

            ####GK QUERY
            gpt = str(int(np.round(np.average(gk.potential))))
            gov = str(int(np.round(np.average(gk.overall))))
            gage = str(int(np.round(np.average(gk.age))))
            if int(gage) >= 35:
                gage = '30'
            else:
                gage = '27'
            SQL_Querygkl = pd.read_sql_query(
                '''SELECT players.short_name,players.team_position,players.age,players.club,
                players.overall,players.potential,players.value_eur,players.wage_eur
                ,players.release_clause_eur,players.contract_valid_until
                FROM players 
                LEFT JOIN teams on teams.Teams = players.club
                where (players.age <= ''' + '\'' + gage + '\'' + ''') 
                and (players.club <> ''' + '\'' + teams + '\'' + ''') 
                and (players.overall > ''' + '\'' + gov + '\'' + ''')
                and (players.potential > ''' + '\'' + gpt + '\'' + ''')
                and(teams.Dprestige  <= ''' + '\'' + tdp + '\'' + '''  and teams.Iprestige  <= ''' + '\'' + tip + '\'' + '''  )
                and (players.team_position in ('GK'))
                and (players.value_eur <=  ''' + '\'' + tbud + '\'' + ''' and  players.release_clause_eur <=  ''' + '\'' + tbud + '\'' + ''');
                ''', con=dbConnection)
            dfgkl = pd.DataFrame(SQL_Querygkl)

            # DEFENCE
            dage = str(int(np.round(np.average(defs.age))))
            if int(dage) >= 29:
                dage = '25'
            else:
                dage = '29'
            dpt = str(int(np.round(np.average(defs.potential))))
            dov = str(int(np.round(np.average(defs.overall))))

            ####DEFENCE QUERY
            SQL_Querydl = pd.read_sql_query(
                '''SELECT players.short_name,players.team_position,players.age,players.club,
                players.overall,players.potential,players.value_eur,players.wage_eur
                ,players.release_clause_eur,players.contract_valid_until
                FROM players 
                LEFT JOIN teams on teams.Teams = players.club
                where (players.age <= ''' + '\'' + dage + '\'' + ''') 
                and (players.club <> ''' + '\'' + teams + '\'' + ''') 
                and (players.overall > ''' + '\'' + dov + '\'' + ''')
                and (players.potential > ''' + '\'' + dpt + '\'' + ''')
                and(teams.Dprestige  <= ''' + '\'' + tdp + '\'' + '''  and teams.Iprestige  <= ''' + '\'' + tip + '\'' + '''  )
                and (players.team_position in ( 'CB' , 'LB' , 'RB' , 'RWB' , 'LWB'))
                and (players.value_eur <=  ''' + '\'' + tbud + '\'' + ''' and  players.release_clause_eur <=  ''' + '\'' + tbud + '\'' + ''');
                ''', con=dbConnection)
            dftdl = pd.DataFrame(SQL_Querydl)

            # MIDFIELD
            mage = str(int(np.round(np.average(mids.age))))
            if int(mage) >= 29:
                mage = '25'
            else:
                mage = '29'
            mpt = str(int(np.round(np.average(mids.potential))))
            mov = str(int(np.round(np.average(mids.overall))))
            ####MIDFIELD QUERY
            SQL_Queryml = pd.read_sql_query(
                '''SELECT players.short_name,players.team_position,players.age,players.club,
                players.overall,players.potential,players.value_eur,players.wage_eur
                ,players.release_clause_eur,players.contract_valid_until
                FROM players 
                LEFT JOIN teams on teams.Teams = players.club
                where (players.age <= ''' + '\'' + mage + '\'' + ''') 
                and (players.club <> ''' + '\'' + teams + '\'' + ''') 
                and (players.overall > ''' + '\'' + mov + '\'' + ''')
                and (players.potential > ''' + '\'' + mpt + '\'' + ''')
                and(teams.Dprestige  <= ''' + '\'' + tdp + '\'' + '''  and teams.Iprestige  <= ''' + '\'' + tip + '\'' + '''  )
                and (players.team_position in ('CM','CDM','CAM'))
                and (players.value_eur <=  ''' + '\'' + tbud + '\'' + ''' and  players.release_clause_eur <=  ''' + '\'' + tbud + '\'' + ''');
                ''', con=dbConnection)
            dftml = pd.DataFrame(SQL_Queryml)
            # ATTACK
            atage = str(int(np.round(np.average(atts.age))))
            if int(atage) >= 29:
                atage = '25'
            else:
                atage = '29'
            apt = str(int(np.round(np.average(atts.potential))))
            aov = str(int(np.round(np.average(atts.overall))))

            ###ATTACK QUERY
            SQL_Queryal = pd.read_sql_query(
                '''SELECT players.short_name,players.team_position,players.age,players.club,
                players.overall,players.potential,players.value_eur,players.wage_eur
                ,players.release_clause_eur,players.contract_valid_until
                FROM players 
                LEFT JOIN teams on teams.Teams = players.club
                where (players.age <= ''' + '\'' + atage + '\'' + ''') 
                and (players.club <> ''' + '\'' + teams + '\'' + ''') 
                and (players.overall >= ''' + '\'' + aov + '\'' + ''')
                and (players.potential >= ''' + '\'' + apt + '\'' + ''')
                and(teams.Dprestige  <= ''' + '\'' + tdp + '\'' + ''' and teams.Iprestige  <= ''' + '\'' + tip + '\'' + '''  )
                and (players.team_position in ('LM','LW','RM','RW','CF','ST'))
                and (players.value_eur <=  ''' + '\'' + tbud + '\'' + ''' and  players.release_clause_eur <=  ''' + '\'' + tbud + '\'' + ''');
                ''', con=dbConnection)
            dftal = pd.DataFrame(SQL_Queryal)
            transfers = pd.concat([dfgkl, dftdl, dftml, dftal])

            #Creating the radar charts
            #goalkeeper radar chart
            plot_urlg=[]
            plot_urld=[]
            plot_urlm=[]
            plot_urla=[]
            for i in range(0, len(dfs)):

                df = pd.DataFrame({
                    'Col A': ['Diving', 'Reflexes', 'Positioning', 'Handling', 'Kicking'],

                    'Col B': dfs[
                        ['goalkeeping_diving', 'goalkeeping_reflexes', 'goalkeeping_positioning', 'goalkeeping_handling',
                         'goalkeeping_kicking']].iloc[i]})

                fig = plt.figure()
                img = io.BytesIO()
                ax = fig.add_subplot(111, projection="polar")

                # theta has 5 different angles, and the first one repeated
                theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                # values has the 5 values from 'Col B', with the first element repeated
                values = df['Col B'].values
                values = np.append(values, values[0])

                # draw the polygon and the mark the points for each angle/value combination
                l1, = ax.plot(theta, values, color="blue", marker="o", label="Name of Col B")
                plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                ax.tick_params(pad=10)  # to increase the distance of the labels to the plot
                # fill the area of the polygon with green and some transparency
                ax.fill(theta, values, 'blue', alpha=0.1)
                plt.title(dfs['short_name'][i])
                fig.savefig(img, format='png')
                img.seek(0)

                plot_urlg.append(base64.b64encode(img.getvalue()).decode())
                #defenders radar chart
            for i in range(0, len(dfde)):
                df = pd.DataFrame({
                    'Col A':['Sprint_speed','Strength','Heading_accuracy','Aggression'
                        ,'Vision','Composure','Reactions',
                        'Short_passing','Long_passing','Crossing','Interceptions','Marking','Slide_tackle',
                             'Stand_tackle'],
                    'Col B': dfde
                            [['movement_sprint_speed','power_strength','attacking_heading_accuracy'
                                ,'mentality_aggression','mentality_vision'
                                , 'mentality_composure','movement_reactions','attacking_short_passing',
                              'skill_long_passing','attacking_crossing','mentality_interceptions','defending_marking'
                                ,'defending_standing_tackle','defending_sliding_tackle']].iloc[i]})

                fig = plt.figure()
                img = io.BytesIO()
                ax = fig.add_subplot(111, projection="polar")
                theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                values = df['Col B'].values
                values = np.append(values, values[0])
                l1, = ax.plot(theta, values, color="green", marker="o", label="Name of Col B")
                plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                ax.tick_params(pad=10)
                ax.fill(theta, values, 'green', alpha=0.1)
                plt.title(dfde['short_name'][i])
                fig.savefig(img, format='png')
                img.seek(0) #saving the image temporarily to avoid taking up space

                plot_urld.append(base64.b64encode(img.getvalue()).decode())
                #midfielders
            for i in range(0, len(dfmid)):
                df = pd.DataFrame({
                    'Col A': ['Heading_accuracy', 'Interceptions', 'Marking','Slide_tackle', 'Stand_tackle',
                              'Aggression', 'Composure', 'Strength', 'Reactions',
                              'Short_passing', 'Long_passing', 'Crossing','Sprint_speed', 'Vision'],
                    'Col B': dfmid[['attacking_heading_accuracy', 'mentality_interceptions', 'defending_marking'
                            , 'defending_standing_tackle',
                   'defending_sliding_tackle', 'mentality_aggression', 'mentality_composure', 'power_strength',
                   'movement_reactions', 'attacking_short_passing', 'skill_long_passing', 'attacking_crossing',
                   'movement_sprint_speed', 'mentality_vision']].iloc[i]})

                fig = plt.figure()
                img = io.BytesIO()
                ax = fig.add_subplot(111, projection="polar")
                theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                values = df['Col B'].values
                values = np.append(values, values[0])
                l1, = ax.plot(theta, values, color="grey", marker="o", label="Name of Col B")
                plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                ax.tick_params(pad=10)
                ax.fill(theta, values, 'grey', alpha=0.1)
                plt.title(dfmid['short_name'][i])
                fig.savefig(img, format='png')
                img.seek(0)  # saving the image temporarily to avoid taking up space

                plot_urlm.append(base64.b64encode(img.getvalue()).decode())
                #attackers
            for i in range(0, len(dfatt)):
                df = pd.DataFrame({
                    'Col A': ['Heading_accuracy','Aggression','Composure', 'Strength'
                                    ,'Reactions','Sprint_speed','Finishing','Penalities'],
                    'Col B': dfatt
                        [['attacking_heading_accuracy', 'mentality_aggression', 'mentality_composure', 'power_strength',
                          'movement_reactions', 'movement_sprint_speed', 'attacking_finishing',
                          'mentality_penalties']].iloc[i]})

                fig = plt.figure()
                img = io.BytesIO()
                ax = fig.add_subplot(111, projection="polar")
                theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
                values = df['Col B'].values
                values = np.append(values, values[0])
                l1, = ax.plot(theta, values, color="purple", marker="o", label="Name of Col B")
                plt.xticks(theta[:-1], df['Col A'], color='grey', size=12)
                ax.tick_params(pad=10)
                ax.fill(theta, values, 'purple', alpha=0.1)
                plt.title(dfatt['short_name'][i])
                fig.savefig(img, format='png')
                img.seek(0)  # saving the image temporarily to avoid taking up space

                plot_urla.append(base64.b64encode(img.getvalue()).decode())
        except IndexError as e:
            return ('Wrong name or team not in the database.Please check your spelling or sofifa website')
        else:
            graphs = [
                # General info
                # Height
                dict(
                    data=[
                        dict(
                            x=height['club'],
                            y=height['height_cm'],
                            type='bar'
                        ),
                    ],
                    layout=dict(
                        title='X axis = Club and Y axis = Average Height'
                        , font=dict(family="Arial")
                    )
                ),
                # Weight
                dict(
                    data=[
                        dict(
                            x=weight['club'],
                            y=weight['weight_kg'],
                            type='bar'
                        ),
                    ],
                    layout=dict(
                        title='X axis = Club and Y axis = Average Height',
                        font=dict(family="Arial")
                    )
                ),
                # Player value
                dict(
                    data=[
                        dict(
                            x=playerve['club'],
                            y=playerve['value_eur'],
                            type='bar'
                        ),
                    ],
                    layout=dict(
                        title='X axis = Club and Y axis = Average players value',
                        font=dict(family="Arial")
                    )),
                # Player wage
                dict(
                    data=[
                        dict(
                            x=playerwe['club'],
                            y=playerwe['wage_eur'],
                            type='bar'
                        ),
                    ],
                    layout=dict(
                        title='X axis = Club and Y axis = Average players wage',
                        font=dict(family="Arial")
                    )),
                #Potential vs overall
                dict(
                    data=[
                        dict(name='Overall',
                            x=dfs['overall'],
                            y=dfs['short_name'],orientation='h',
                            type='bar'
                        ),dict(name='Potential',
                            x=dfs['potential'],
                            y=dfs['short_name'],orientation='h',
                            type='bar'
                        )
                    ],
                    layout=dict(
                        title='X Axis=Goalkeepers and Y Axis = Rating',
                        font=dict(family="Arial")
                    )
                    #Reflexes vs positioning
                ),dict(data=[dict(x=dfgk['goalkeeping_reflexes'],
                                  y=dfgk['goalkeeping_positioning'],
              mode='markers', text=dfgk['short_name'], marker=dict(size=8, color=dfgk['color']),type='scatter')]
                       ,layout=dict(
                        title='X Axis = Reflexes and Y Axis = Positioning',
                        font=dict(family="Arial"))),
                #Handling vs Diving
                       dict(data=[dict(x=dfgk['goalkeeping_handling'],
                                y=dfgk['goalkeeping_diving'],
                                text=dfgk['short_name'],mode='markers',
                            marker=dict(size=8, color=dfgk['color']), type='scatter')],layout=dict(
                           title='X Axis = Handling and Y Axis = Diving',
                           font=dict(family="Arial"))),
                        #Kicking
                        dict(
                        data=[
                            dict(
                                x=dfgk['short_name'],
                                y=dfgk['goalkeeping_kicking'],
                                type='bar'
                            ),
                        ],
                        layout=dict(
                            title='X Axis = Player Name and Y Axis = Kicking',
                            font=dict(family="Arial"))),
                            # Overall vs potential for defenders
                    dict(data=[
                        dict(name='Overall',
                             x=dfde['overall'],
                             y=dfde['short_name'], orientation='h',
                             type='bar'), dict(name='Potential',
                                               x=dfde['potential'],
                                               y=dfde['short_name'], orientation='h',
                                               type='bar')], layout=dict(
                        title='X Axis = Rating and Y Axis = Players'
                        , font=dict(family="Arial"))),
                    # Heading
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['attacking_heading_accuracy']
                                    , type='bar')], layout=dict(
                        title='X Axis = Players  and Y Axis = Heading', font=dict(family="Arial"))),
                    # Aggression
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['mentality_aggression']
                                    , type='bar'), ], layout=dict(
                        title='X Axis = Players and Y Axis = Aggression', font=dict(family="Arial"))),
                    # Composure
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['mentality_composure']
                                    , type='bar')], layout=dict(
                        title='X Axis = Players  and Y Axis = Composure', font=dict(family="Arial"))),
                    # Strength
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['power_strength']
                                    , type='bar'), ], layout=dict(
                        title='X Axis = Players and Y Axis = Strength', font=dict(family="Arial"))),
                    # Reactions
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['movement_reactions']
                                    , type='bar')], layout=dict(
                        title='X Axis = Players and Y Axis = Reactions', font=dict(family="Arial"))),
                    # Jumping
                    dict(data=[dict(x=dfdea['short_name'], y=dfdea['power_jumping']
                                    , type='bar')], layout=dict(
                        title='X Axis = Players and Y Axis = Jumping', font=dict(family="Arial"))),
                    # Interceptions versus Marking
                    dict(data=[dict(x=dfdea['mentality_interceptions'],
                                    y=dfdea['defending_marking'],
                                    text=dfdea['short_name'], mode='markers',
                                    marker=dict(size=8, color=dfdea['color']), type='scatter')], layout=dict(
                        title='X Axis = Interceptions and Y Axis = Marking',font=dict(family="Arial"))),
                    # Stand tackle versus slide tackle
                    dict(data=[dict(x=dfdea['defending_standing_tackle'],
                                    y=dfdea['defending_sliding_tackle'],
                                    text=dfdea['short_name'], mode='markers',
                                    marker=dict(size=8, color=dfdea['color']), type='scatter')], layout=dict(
                        title='X Axis = Stand tackle and Y Axis = Slide tackle',
                        font=dict(family="Arial"))),
                    # Short passing versus long passing
                    dict(data=[dict(x=dfdea['attacking_short_passing'],
                                    y=dfdea['skill_long_passing'],
                                    text=dfdea['short_name'], mode='markers',
                                    marker=dict(size=8, color=dfdea['color']), type='scatter')], layout=dict(
                        title='X Axis = Short passing and Y Axis = long passing',
                        font=dict(family="Arial"))),
                # Overall vs potential midfielders
                dict(data=[
                    dict(name='Overall',
                         x=dfmid['overall'],
                         y=dfmid['short_name'], orientation='h',
                         type='bar'
                         ), dict(name='Potential',
                                 x=dfmid['potential'],
                                 y=dfmid['short_name'], orientation='h',
                                 type='bar')], layout=dict(
                    title='X Axis = Rating and Y Axis = Players', font=dict(family="Arial"))),
                # Aggression
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['mentality_aggression']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Aggression', font=dict(family="Arial"))),
                # Composure
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['mentality_composure']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Composure', font=dict(family="Arial"))),
                # Strength
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['power_strength']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Strength', font=dict(family="Arial"))),
                # Vision
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['mentality_vision']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Vision', font=dict(family="Arial"))),
                # Finishing
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['attacking_finishing']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Finishing', font=dict(family="Arial"))),
                # Long shots
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['power_long_shots']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Long Shots', font=dict(family="Arial"))),
                # Dribbling
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['skill_dribbling']
                                , type='bar')], layout=dict(
                    title='X Axis = Players and Y Axis = Dribbling', font=dict(family="Arial"))),
                # Interceptions versus Marking midfielders
                dict(data=[dict(x=dfmida['mentality_interceptions'],
                                y=dfmida['defending_marking'],
                           text = dfmida['short_name'], mode = 'markers',
                 marker = dict(size=8, color=dfmida['color']), type = 'scatter')], layout = dict(
                title='X Axis = Interceptions and Y Axis = Marking',font=dict(family="Arial"))),
            # Agility versus balance
            dict(data=[dict(x=dfmida['movement_agility'], y=dfmida['movement_balance'], mode='markers',
                            text=dfmida['short_name']
                , marker = dict(size=8, color=dfmida['color']), type = 'scatter')],layout = dict(
                title='X Axis = Agility and Y Axis = Balance', yaxis_title='Slide tackle',
                font=dict(family="Arial"))),
            # Stand tackle versus slide tackle
            dict(data=[dict(x=dfmida['defending_standing_tackle'],
                            y=dfmida['defending_sliding_tackle'],
                       text = dfmida['short_name'], mode = 'markers',
            marker = dict(size=8, color=dfmida['color']), type = 'scatter')], layout = dict(
                title='X Axis = Stand tackle and Y Axis = Slide tackle',
                font=dict(family="Arial"))),
            # Short passing versus long passing
            dict(data=[dict(x=dfmida['attacking_short_passing'],
                            y=dfmida['skill_long_passing'],
                       text = dfmida['short_name'], mode = 'markers',
            marker = dict(size=8, color=dfdea['color']), type = 'scatter')], layout = dict(
                title='X Axis = Short passing and Y Axis = long passing',
                font=dict(family="Arial"))),
                # Overall vs potential attackers
                dict(data=[
                    dict(name='Overall',
                         x=dfatt['overall'],
                         y=dfatt['short_name'], orientation='h',
                         type='bar'
                         ), dict(name='Potential',
                                 x=dfatt['potential'],
                                 y=dfatt['short_name'], orientation='h',
                                 type='bar')], layout=dict(
                    title='X Axis = Rating and Y Axis = Players', font=dict(family="Arial"))),
                # Aggression
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['mentality_aggression']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Aggression', font=dict(family="Arial"))),
                # Composure
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['mentality_composure']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Composure', font=dict(family="Arial"))),
                # Strength
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['power_strength']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Strength', font=dict(family="Arial"))),
                # Heading
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['attacking_heading_accuracy']
                                , type='bar') ], layout=dict(
                    title='X Axis = Players and Y Axis = Heading', font=dict(family="Arial"))),
                # Volleys
                dict(data=[dict(x=dfmida['short_name'], y=dfmida['attacking_finishing']
                                , type='bar')], layout=dict(
                    title='X Axis = Players and Y Axis = Volleys', font=dict(family="Arial"))),
                # Penalties
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['mentality_penalties']
                                , type='bar')], layout=dict(
                    title='X Axis = Players and Y Axis = Penalties', font=dict(family="Arial"))),
                # Dribbling
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['skill_dribbling']
                                , type='bar')], layout=dict(
                    title='X Axis = Players and Y Axis = Dribbling', font=dict(family="Arial"))),
            # sprint speed
                dict(data=[dict(x=dfatta['short_name'], y=dfatta['movement_sprint_speed']
                            , type='bar')], layout=dict(
                title='X Axis = Players and Y Axis = Sprint speed', font=dict(family="Arial"))),
            # jumping
            dict(data=[dict(x=dfatta['short_name'], y=dfatta['power_jumping'], type='bar')], layout=dict(
                title='X Axis = Players and Y Axis = Jumping', font=dict(family="Arial"))),
            # Agility versus balance
            dict(data=[dict(x=dfatta['movement_agility'], y=dfatta['movement_balance'], mode='markers',
                text = dfatta['short_name'], marker = dict(size=8,color=dfatta['color']), type = 'scatter')],
                layout = dict(title='X Axis = Agility and Y Axis = Balance',font=dict(family="Arial"))),
            # Finishing versus positioning
            dict(data=[dict(x=dfatta['attacking_finishing'],
                            y=dfatta['mentality_positioning'],
                       text = dfatta['short_name'], mode = 'markers', marker = dict(size=8, color=dfatta[
                'color']),xaxis_title='Finishing', yaxis_title='Positioning',type = 'scatter')],layout = dict(
                title='X Axis = Finishing and Y Axis = Positioning' ,font=dict(family="Arial")))
            ]

            title =['Average height for clubs in ' + league, 'Average weight for clubs in ' + league,
             'Average players value for clubs in ' + league,'Average players wage for clubs in ' + league, 'Goalkeepers',
                    'Reflexes versus positioning for goalkeepers in the'+league,'Handling versus diving for goalkeepers in the'+league,
             'Kicking for goalkeepers in'+league,'Defenders','Heading for defenders in the ' + league, 'Aggression for defenders in the ' + league,
                     'Composure for defenders in the ' + league, 'Strength for defenders in the' + league,
                      'Reactions for defenders in the ' + league, 'Jumping for defenders in the ' + league,
                      'Interceptions versus Marking for defenders in the' + league
                     , 'Stand tackle versus slide tackle for defenders in the' + league,
                     'Short passing versus long passing for defenders in the' + league,
                      'Midfielders', 'Aggression for midfielders in the ' + league, 'Composure for midfielders in the ' + league
                      , 'Strength for midfielders in the ' + league,
                       'Vision for midfielders in the ' + league, 'Finishing for midfielders in the ' + league
                       , 'Long shots for midfielders in the ' + league, 'Dribbling for midfielders in the ' + league,
                        'Interceptions versus Marking for midfielders in the' + league, 'Agility versus balance for midfielders in the' + league
                        , 'Stand tackle versus slide tackle for midfielders in the' + league, 'Short passing versus long passing for midfielders in the' + league,'Attackers'
                     , 'Aggression for attackers in the ' + league, 'Composure for attackers in the' + league,
                      'Strength for attackers in the ' + league, 'Heading for attackers in the ' + league,
                      'Volleys for attackers in the ' + league,'Penalties for attackers in the ' + league,
                       'Dribbling for attackers in the ' + league, 'Sprint speed for attackers in the ' + league
                       , 'Jumping for attackers in the ' + league, 'Agility versus balance for attackers in the' + league,
                        'Finishing versus positioning for attackers in the' + league]
            ids = [title[i].format(i) for i, _ in enumerate(graphs)]


            #ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
            # Convert the figures to JSON
            graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


        return render_template('/tresults.html', data=[transfers.to_html()], team=teams,ids=ids, graphJSON=graphJSON
                               ,plot_urlg=plot_urlg,plot_urld=plot_urld,plot_urlm=plot_urlm,plot_urla=plot_urla)
    else:
        return render_template('/teamsda.html')

if __name__ == '__main__':
    app.run(debug=True)
