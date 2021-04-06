# Importing libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Getting the dataset and doing some pre-processing
df = pd.read_csv('tech_raw.csv')
df.Working_Experience_Aggregated.replace(to_replace='0 Years', value='0 - 3 years', inplace=True)
job_perk = ['Job_Perk_Meals_allowance/Company_provided_meals_or_snacks',
            'Job_Perk_Transportation_benefit',
            'Job_Perk_Health_benefits',
            'Job_Perk_Fitness_or_wellness_benefit_(ex._gym_membership)',
            'Job_Perk_Computer/_Office_equipment_allowance',
            'Job_Perk_Professional_development_sponsorship',
            'Job_Perk_Annual_bonus',
            'Job_Perk_Long-term_leave',
            'Job_Perk_Parental_leave',
            'Job_Perk_Stock_options_or_shares',
            'Job_Perk_Education_sponsorship',
            'Job_Perk_Child_care']
job_options = [
    {'value': 'todos', 'label': 'Show all'},
    {'value': 'Technical Team Leader', 'label': 'Technical Team Leader'},
    {'value': 'Full-Stack Developer', 'label': 'Full-Stack Developer'},
    {'value': 'Product Owner/Product Manager', 'label': 'Product Owner/Product Manager'},
    {'value': 'Back-End Developer', 'label': 'Back-End Developer'},
    {'value': 'Mobile Apps Developer', 'label': 'Mobile Apps Developer'},
    {'value': 'Front-End Developer', 'label': 'Front-End Developer'},
    {'value': 'Project Manager', 'label': 'Project Manager'},
    {'value': 'Business Applications (BI/CRM/ERP)', 'label': 'Business Applications (BI/CRM/ERP)'},
    {'value': 'DevOps Engineer', 'label': 'DevOps Engineer'},
    {'value': 'Data Scientist/Data Engineer', 'label': 'Data Scientist/Data Engineer'},
    {'value': 'Computer & Network Security', 'label': 'Computer & Network Security'},
    {'value': 'Quality Assurance/Testing', 'label': 'Quality Assurance/Testing'},
    {'value': 'CTO', 'label': 'CTO'},
    {'value': 'UX/UI Designer', 'label': 'UX/UI Designer'},
    {'value': 'Scrum Master', 'label': 'Scrum Master'},
    {'value': 'Solutions Architect', 'label': 'Solutions Architect'},
    {'value': 'SysAdmin Engineer', 'label': 'SysAdmin Engineer'}
]
job_motivator = ['Job_Motivator_Work_life_balance',
                 'Job_Motivator_Training/Development_programs_at_work',
                 'Job_Motivator_Career_growth_opportunities',
                 'Job_Motivator_Remote_working',
                 'Job_Motivator_Flexible_schedule',
                 'Job_Motivator_Company_culture',
                 "Job_Motivator_The_technologies_I'm_working_with",
                 'Job_Motivator_Versatility/Variety_of_projects',
                 'Job_Motivator_Freedom_to_choose_the_clients_and/or_projects',
                 'Job_Motivator_Being_autonomous_at_work',
                 'Job_Motivator_How_widely_used_or_impactful_the_product/service_I_work_on_is',
                 'Job_Motivator_Environmentally_friendly/responsible_work_practice']

df['Job_Perk_Avg'] = round(df[job_perk].mean(axis=1) / 7.0 * 10, 1)
df['Job_Motivator_Avg'] = round(df[job_motivator].mean(axis=1) / 7.0 * 10, 1)
df['Employer_Industry'].replace('Software development - other', 'Software development', inplace=True)
df['Count'] = 1
df['Employer_Industry'].replace('Software development', 'Software Dev.', inplace=True)
df['Employer_Industry'].replace('Financial and banking', 'Finance', inplace=True)
df['Employer_Industry'].replace('Information technology', 'IT', inplace=True)
df['Employer_Industry'].replace('Cloud-based solutions or services', 'Cloud solutions', inplace=True)
df['Employer_Industry'].replace('Data and analytics', 'Analytics', inplace=True)
df['Employer_Industry'].replace('Web development or design', 'Web design', inplace=True)
df['Employer_Industry'].replace('Retail or ecommerce', 'Retail', inplace=True)
df['Employer_Industry'].replace('Telecommunications', 'Telecom', inplace=True)
df['Employer_Industry'].replace('Government or public administration', 'Government', inplace=True)
df['Employer_Industry'].replace('Research - academic or scientific', 'Research', inplace=True)
df['Employer_Industry'].replace('Media, advertising, publishing, or entertainment', 'Media & Adversiting', inplace=True)
df['Employer_Industry'].replace('Education and training', 'Education', inplace=True)
df['Employer_Industry'].replace('Healthcare or social services', 'Health & Social', inplace=True)
df['Employer_Industry'].replace('Software as a service (saas) development', 'SaaS Dev.', inplace=True)
df_tech = df.dropna(axis=0, how='any',
                    thresh=None,
                    subset=['Way_Into_Tech', 'Education_Level', 'Work_Company_Country', 'Avg_Salary', 'Age',
                            'Working_Experience_Aggregated'])
df_tech.set_index('Job_Role_Original', inplace=True)
# Creating the App and the Layout
app = dash.Dash(__name__)

server = app.server
app.title = 'Tech Jobs in Portugal'
app.layout = html.Div(children=[

    html.Div(children=[
        html.Img(src=app.get_asset_url('landingjobs.png'),
                 style={'width': '60%', 'padding-left':'5%', 'margin': '0.5%', 'align': 'center'}, ),
        html.Hr(),
        html.Div(children=[
            html.H3('Select the Job Role you want to see:',
                    style={'width': '35%', 'align': 'center', 'justify': 'center'}),
            dcc.Dropdown(id='job', value='todos', multi=False,
                         options=job_options, clearable=False,
                         searchable=True, placeholder='Show all', style={'width': '60%'}),
        ], style={'display': 'flex', 'justify_items': 'center'}),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[dcc.Graph(id='graph_piechart', figure={}, style={'width': '100%', 'align': 'top', 'justify': 'center',
                                        'vertical-align': 'middle'})],
                                 style={'width': '85%', 'align': 'top', 'justify': 'center',
                                        'vertical-align': 'middle'}),
                        #  html.Br(),
                    ])], style={'width': '25%', 'align': 'center', 'justify': 'center', 'vertical-align': 'middle'},
                    className='smalltextbox'),
                html.Div(children=[dcc.Graph(id='graph_sunburst', figure={}), ],
                         style={'width': '25%', 'align': 'center', 'justify': 'center', 'vertical-align': 'middle'},
                         className='smalltextbox'),
                html.Div(children=[
                    dcc.Graph(id='graph_geoplot', figure={})],
                    style={'width': '50%', 'align': 'center', 'justify': 'center'}, className='smalltextbox'), ],
                style={'display': 'flex', 'height': '30%'}, className='smallbox'), ],
        ),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    # html.H6('CARTÃO'
                    #        'Average Salary'),
                    html.Div(children=[
                        dcc.Graph(id='graph_barplot', figure={})
                    ])], style={'width': '45%', 'align': 'bottom', 'justify': 'bottom'}, className='smalltextbox'),

                html.Div(children=[
                    dcc.Graph(id='graph_heatmap_continent_salaryfairness_changejobs', figure={})],
                    style={'width': '100%', 'align': 'right'}, className='smalltextbox'), ],
                style={'display': 'flex'}, className='smallbox'), ],
        ), ]),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(id='graph_barplot_contractor_permanent', figure={})
        ], style={'width': '20%', 'align': 'left'}, className='smalltextbox'),

        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='graph_radiochart_perk', figure={})
            ], style={'width': '100%', 'align': 'center', 'justify': 'center'},
                className='smalltextbox'),
            html.Div(children=[
                dcc.Graph(id='graph_radiochart_motivation', figure={})
            ], style={'width': '100%', 'align': 'center', 'justify': 'right'},
                className='smalltextbox'),
        ], style={'width': '50%'}),
        html.Div(children=[
            dcc.Graph(id='graph_histogram_gendergap', figure={}),
        ], style={'width': '20%', 'align': 'right', 'vertical-align': 'middle', 'justify': 'center'},
            className='smalltextbox'),
    ], style={'display': 'flex', 'align': 'right'}, className='smallbox'),

    html.Div(children=[
        dcc.Graph(id='graph_treemap', figure={})], className='smallbox'),
], )


@app.callback(Output('graph_geoplot', 'figure'), [Input('job', 'value')])
def fifth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    data_choropleth = dict(type='choropleth',
                           locations=filtered_job['Work_Company_Country'].value_counts().index,
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=np.log(filtered_job['Work_Company_Country'].value_counts().values),
                           text=filtered_job['Work_Company_Country'].value_counts().index,
                           colorscale='Bluyl',
                           customdata=filtered_job['Work_Company_Country'].value_counts().values,
                           hovertemplate="Country: <b>%{text}</b> <br>" +
                                         "Job Positions: %{customdata} Employees<br><extra></extra>",
                           showscale=False
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type='natural earth'
                                                      ),
                                      showland=True,  # default = True
                                      landcolor='lightgrey',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure'
                                      ),

                             title=dict(text='Where are the hiring companies?',
                                        x=.5  # Title relative position according to the xaxis, range (0,1)
                                        )
                             )
    fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig_choropleth.update_layout(margin=dict(t=30, b=0, l=0, r=0), font_family="Gill Sans MT",
                                 title_font_family="Gill Sans MT")
    return fig_choropleth


@app.callback(Output('graph_piechart', 'figure'), [Input('job', 'value')])
def seventh_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = px.pie(filtered_job, names='Way_Into_Tech', title='How to get into Tech?',
                 labels={'Way_Into_Tech': 'Way Into Tech'},
                 color_discrete_sequence=px.colors.sequential.Aggrnyl,
                 )
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    fig.update_layout(margin=dict(t=30, b=0, l=5, r=5), font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT")
    return fig


@app.callback(Output('graph_heatmap_continent_salaryfairness_changejobs', 'figure'), [Input('job', 'value')])
def fifth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = go.Figure(data=go.Heatmap(
        z=filtered_job[
            filtered_job['Employer_Industry'].isin(filtered_job.Employer_Industry.value_counts()[:5].index.values)][
            'Avg_Salary'],
        x=filtered_job[
            filtered_job['Employer_Industry'].isin(filtered_job.Employer_Industry.value_counts()[:5].index.values)][
            'Employer_Industry'],
        y=filtered_job[
            filtered_job['Employer_Industry'].isin(filtered_job.Employer_Industry.value_counts()[:5].index.values)][
            'Changing_Jobs_next_6_months'],
        colorscale='Bluyl',
        text=filtered_job[
            filtered_job['Employer_Industry'].isin(filtered_job.Employer_Industry.value_counts()[:5].index.values)][
            'Employer_Industry'],
        hovertemplate=
        "Industry: %{text}<br>" +
        "Willingness to Change Job: %{y:,.0f}<br>" +
        "Average Salary: %{z:,.0f}<br>" +
        "<extra></extra>")).update_xaxes(categoryorder="category ascending")
    fig.update_layout(title='Does Average Salary (Color Encoded) influence willingness to Change Job by Sector?',
                      yaxis_title='Willingness to Change Job',
                      xaxis_title='Sector',
                      xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      margin=dict(t=30, b=20, l=20, r=30), font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT")
    return fig


@app.callback(Output('graph_barplot', 'figure'), [Input('job', 'value')])
def eight_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = px.histogram(filtered_job[filtered_job['Employer_Industry']
                       .isin(filtered_job.Employer_Industry.value_counts()[:5].index.values)],
                       title='Average Salary per Industry',
                       x="Avg_Salary", y="Employer_Industry",  # color="Working_Experience_Aggregated",
                       histfunc='avg',
                       # category_orders={'Working_Experience_Aggregated': ['0 - 3 years', '3 - 6 years', '6+ years']},
                       color_discrete_sequence=px.colors.sequential.Bluyl
                       ).update_yaxes(categoryorder="total ascending")  # , ticklabelposition="inside")

    fig.update_traces(hovertemplate="Average Salary: %{x:,.0f}")
    fig.update_layout(xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      yaxis_title='',
                      xaxis_title='Average Salary',
                      margin=dict(t=30, b=0, l=0, r=0),
                      font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT"
                      )
    return fig


@app.callback(Output('graph_treemap', 'figure'), [Input('job', 'value')])
def ninth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = px.treemap(filtered_job[filtered_job['Employer_Industry'].isin(
        filtered_job.Employer_Industry.value_counts()[:5].index.values)],
                     path=['Residence_District_Aggregated', 'Employer_Industry'],
                     color_discrete_sequence=px.colors.sequential.Aggrnyl,
                     title='Treemap of Most important Sectors per District')
    fig.update_layout(hovermode=False,
                      margin=dict(t=40, b=0, l=0, r=0),
                      font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT",
                      title_yanchor="top",
                      title_xanchor="left",
                      title_y=0.96,
                      title_x=0.02,
                      )
    return fig


@app.callback(Output('graph_barplot_contractor_permanent', 'figure'), [Input('job', 'value')])
def tenth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech

    fig = px.histogram(filtered_job, title='Seniority effect on Contract?',
                       y='Count', x="Working_Experience_Aggregated", color="Employment_Status_Aggregated",
                       histfunc='sum',
                       barmode='relative',
                       # category_orders={'Working_Experience_Aggregated': ['0 - 3 years', '3 - 6 years', '6+ years']},
                       color_discrete_sequence=px.colors.sequential.Bluyl,
                       orientation='v').update_xaxes(
        categoryorder="category ascending")

    # fig.update_traces(hovertemplate=": %{x:,.0f}")
    fig.update_layout(xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      yaxis_title='Count of Employees',
                      xaxis_title='Working Experience',
                      hovermode=False,
                      )
    fig.update_layout(legend_font_size=10,
                      legend_title='',
                      legend_traceorder="reversed",
                      legend=dict(
                          yanchor="top",
                          y=0.98,
                          xanchor="left",
                          x=0.03)
                      , font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT",
                      margin=dict(t=45, b=0, l=20, r=0))

    return fig


@app.callback(Output('graph_radiochart_perk', 'figure'), [Input('job', 'value')])
def eleventh_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech

    Job_P = ['Meals_allowance/Company_provided_meals_or_snacks', 'Transportation_benefit', 'Health_benefits',
             'Fitness_or_wellness_benefit_(ex._gym_membership)', 'Computer/_Office_equipment_allowance',
             'Professional_development_sponsorship', 'Annual_bonus', 'Long-term_leave', 'Parental_leave',
             'Stock_options_or_shares', 'Education_sponsorship', 'Child_care']

    Job_Perk_ = []
    for job in Job_P:
        Job_Perk_ = np.append(Job_Perk_, ('Job_Perk_' + job))

    r = []
    for job_pe in Job_Perk_:
        r = np.append(r, filtered_job[job_pe].median() / 7 * 5)

    dffff = pd.DataFrame(dict(r=r, theta=Job_P))

    dffff.replace('Meals_allowance/Company_provided_meals_or_snacks', "Food Allowance", inplace=True)
    dffff.replace('Transportation_benefit', "Transportation", inplace=True)
    dffff.replace('Health_benefits', "Health Plans", inplace=True)
    dffff.replace('Fitness_or_wellness_benefit_(ex._gym_membership)', "Fitness benefits", inplace=True)
    dffff.replace('Computer/_Office_equipment_allowance', "Equipment Allowance", inplace=True)
    dffff.replace('Professional_development_sponsorship', "Professional Education", inplace=True)
    dffff.replace('Annual_bonus', "Annual Bonus", inplace=True)
    dffff.replace('Long-term_leave', "Long-term Leave", inplace=True)
    dffff.replace('Parental_leave', "Parental Leave", inplace=True)
    dffff.replace('Stock_options_or_shares', "Stock Options", inplace=True)
    dffff.replace('Education_sponsorship', "Education Sponsorship", inplace=True)
    dffff.replace('Child_care', "Child Care", inplace=True)

    # dft = pd.DataFrame(pd.Series(r))
    # dft.rename({0: 'r'}, axis=1, inplace=True)
    # dft['theta'] = dffff.theta.values

    fig = px.line_polar(dffff, r='r', theta='theta', line_close=True,
                        title='Job Perks Satisfaction',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        height=250)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                showticklabels=False, ticks=''
            ),
            angularaxis=dict(
                visible=True,

            ),
        ),
        showlegend=False,
        hovermode=False,
        font_family="Gill Sans MT",
        title_font_family="Gill Sans MT",
        margin=dict(t=80, b=40, l=140, r=140)
    )
    fig.update_traces(fill='tonext')
    return fig


@app.callback(Output('graph_radiochart_motivation', 'figure'), [Input('job', 'value')])
def twelfth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    Job_Mot = ['Work_life_balance', 'Compensation_and_benefits', 'Training/Development_programs_at_work',
               'Career_growth_opportunities', 'Remote_working', 'Flexible_schedule',
               'Company_culture', "The_technologies_I'm_working_with", 'Versatility/Variety_of_projects',
               'Freedom_to_choose_the_clients_and/or_projects', 'Being_autonomous_at_work',
               'How_widely_used_or_impactful_the_product/service_I_work_on_is',
               'Environmentally_friendly/responsible_work_practice']

    # creating array with colloms names
    Job_Motivator_ = []
    for jbm in Job_Mot:
        Job_Motivator_ = np.append(Job_Motivator_, ('Job_Motivator_' + jbm))

    # creating array with average value per collom
    rm = []
    for job_mot in Job_Motivator_:
        rm = np.append(rm, filtered_job[job_mot].median() / 7 * 5)

    dfff = pd.DataFrame(dict(rm=rm, thetam=Job_Mot))

    dfff.replace('Work_life_balance', "Work-Life Balance", inplace=True)
    dfff.replace('Compensation_and_benefits', "Salary & Benefits", inplace=True)
    dfff.replace('Training/Development_programs_at_work', "Training & Development at Work", inplace=True)
    dfff.replace('Career_growth_opportunities', "Career Growth Opportunities", inplace=True)
    dfff.replace('Remote_working', "Remote Work", inplace=True)
    dfff.replace('Flexible_schedule', "Flexible Schedule", inplace=True)
    dfff.replace('Company_culture', "Company Culture", inplace=True)
    dfff.replace("The_technologies_I'm_working_with", "Technologies I work with", inplace=True)
    dfff.replace('Versatility/Variety_of_projects', "Variety of projects", inplace=True)
    dfff.replace('Freedom_to_choose_the_clients_and/or_projects', "Decision Freedom", inplace=True)
    dfff.replace('Being_autonomous_at_work', "Autonomy", inplace=True)
    dfff.replace('How_widely_used_or_impactful_the_product/service_I_work_on_is', "Impact in the world", inplace=True)
    dfff.replace('Environmentally_friendly/responsible_work_practice', "Company Purpose", inplace=True)

    dftt = pd.DataFrame(pd.Series(rm))
    dftt.rename({0: 'rm'}, axis=1, inplace=True)
    dftt['thetam'] = dfff.thetam.values

    fig = px.line_polar(dftt, r='rm', theta='thetam', line_close=True,
                        title='How much satisfaction do these Job aspects bring me?',
                        color_discrete_sequence=px.colors.sequential.Bluyl, height=250)
    # symbol='markers',
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                showticklabels=False, ticks=''
            ),
            angularaxis=dict(
                visible=True,

            ),
        ),
        showlegend=False,
        hovermode=False,
        font_family="Gill Sans MT",
        title_font_family="Gill Sans MT",
        margin=dict(t=80, b=40, l=140, r=140)
    )
    fig.update_traces(fill='tonext')
    return fig


@app.callback(Output('graph_sunburst', 'figure'), [Input('job', 'value')])
def thirteenth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = px.sunburst(filtered_job[filtered_job['Employer_Industry'].isin(
        filtered_job.Employer_Industry.value_counts()[:4].index.values)],
                      path=['Employer_Industry', 'Gender', ], color='Employer_Industry',
                      color_discrete_sequence=px.colors.sequential.Aggrnyl,
                      title='Sector Gender Breakdown',
                      )  # values='Avg_Salary')
    fig.update_layout(hovermode=False, margin=dict(t=30, b=0, l=5, r=5), font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT")

    return fig


@app.callback(Output('graph_histogram_gendergap', 'figure'), [Input('job', 'value')])
def fourteenth_plot(job):
    if job != 'todos':
        filtered_job = df_tech.loc[[job]]
    else:
        filtered_job = df_tech
    fig = px.histogram(filtered_job[filtered_job.Avg_Salary > 10000], x='Avg_Salary', y='Count',
                       color='Gender', histfunc='sum', orientation='v', nbins=12,
                       color_discrete_sequence=px.colors.sequential.Aggrnyl + px.colors.sequential.Bluyl,
                       title='Salary Gender Breakdown')
    fig.update_traces(hovertemplate="Average Salary: <b>%{x:,.0f}<br></b>" + "Count: <b>%{y:,.0f}</b>")
    fig.update_layout(xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      yaxis_title='Count of Employees',
                      xaxis_title='Average Salary',
                      margin=dict(t=45, b=0, l=0, r=0),
                      legend=dict(
                          yanchor="top",
                          y=1.00,
                          xanchor="left",
                          x=0.50,
                      ),
                      legend_font_size=10,
                      legend_title='',
                      legend_traceorder="reversed",
                      font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT"
                      )
    return fig


if __name__ == '__main__':
    app.run_server()