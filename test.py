#!/usr/bin/env python
# coding: utf-8

# In[1]:


#data cleaning and functions
import pandas as pd

df = pd.read_csv("Absenteeism_at_work_Project.csv")

df.head()

#average number of absence for all employees
def absence(data):
    df = data
    df_abs_cnt = df.groupby("ID").size().reset_index()

    df_abs_cnt.columns = ["ID", "Count"]

    return round(df_abs_cnt["Count"].mean())
absence(df)

df2 = df

#Eda on dataset
df2["Education"] = df2["Education"].replace({1.0 :"High School", 2.0 :'Graduate', 3.0 : "Postgraduate", 4.0: "Doctor"})

#Day of week absent
def age(df):
    df = df[df["ID"] == 11]
    return max(df["Age"])
age(df)

df2["Disciplinary failure"] = df2["Disciplinary failure"].replace({1.0: "Yes", 0.0 : "No"})
df2.head()

#read hr
#read new hr data
hr = pd.read_csv("Hr.csv")

hr.head()


hr["Year"] = pd.DatetimeIndex(hr['Date']).year

hr.head()


# In[8]:


#import all libraries
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_table
import plotly.graph_objects as go

#dash start up
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

server = app.server
 
##########App Layout

#Build the top layout with the employee absentee info
app.layout = html.Div(style={'background-color': "#f9f9f9", 
                            "overflow-x" : "hidden",
                            "margin-right" : "0px"}, children = [
    html.Br(),
    html.Div(
                    [html.Img(
                            src=("static\images\logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "10px",
                                "margin-left" : "30px"
                            },
                        ),
                     html.H3("HR Analytics Dashboard", style = {"display" : "inline-block",
                                            "margin-left" : "400px"}),
                     
                        html.A(
                            html.Button(html.H5("Learn More"), id="learn-more-button",
                  style = { "text-align": "center",
                  "height": "100%",
                  "text-transform": "none",
                  "font-size": "10px",
                  "float": "right",
                  "margin-right": "30px",
                  "margin-top": "10px",
                  'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                  "border-radius": "5px",
                  "background-color": "#f9f9f9",
                  "border": "2px solid #e7e7e7"}),
                            href="https://pairview.co.uk/",
                        )
                    ],
                    className="one-third column",
                    id="button",
        
                ),
    html.Div(html.H4(html.P("A Pairview Solution"), style = {"display" : "block",
                                                            "display" : "inline-block",
                                                            "margin-left" : "620px"})),
    #html.Br(),
    #html.Br(),
    #html.Br(),
    dbc.Row([
        dbc.Col
        (
            dcc.Input(
            id = "Input_Id",
            type = "number",
            placeholder = "Enter Employee Id:",
             style= {"width" : "19.7rem", "border-radius" : 10, "display" : "flex", "background-color" : "#f9f9f9",
                    "text-align" : "justify"}),
         style = {"left" : "30px"})
            ]),
    html.Br(),
            #html.Div([html.H3(id = "out"), html.P("No of inputs")],
             #   id = "outer"),
    html.Br(),
    #Establish a row that will contain major info about the inputed customer
    dbc.Container(fluid=True,
                  children = [
    dbc.Row([
        #A card on employee Image and other descriptions
        dbc.Col( 
            dbc.Card(
    [
        dbc.CardImg(src="static/images/Web-Scraping-600x204 - Copy.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("How to Use", className="card-title"),
                html.P(
                    "This is an HR Dashboard capable of providing Employee Information"),
                html.P(
                    "Input an Employee ID and it provides high level information",
                    className="card-text")
            ]
        ),
    ],
    style={"width": "103%",
           "height" : "90%",
          "left" : "15px",
          "background-color": "#f9f9f9",
          "margin-bottom" : "45px"},
),   width = 3),
        
        #major Abst days and age
        dbc.Col([
        html.Div([html.H5(id = "Absentee_guage"), html.P("Absent Days")],
                id="absent", className = "mini-container",
                style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
            html.Br(),
            html.Br(),
        html.Div([html.H5(id = "Emp Age"), html.P("Current Age")],
                id="absent2", className = "mini-container2",
                style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"})
        ], width = 2),
        
        #Height and Distance
        dbc.Col([
            html.Div([html.H5(id = "Emp Height"), html.P("Current Height")],
                    id = "current Height", className = "mini-container",
                style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.Div([html.H5(id = "Emp Distance"), html.P("Work-Distance")],
                    id = "current Weight", className = "mini-container",
                style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"})
        ], width = 2),
        
        #weight and absent hours
        dbc.Col([html.Div([html.H5(id = "Emp Weight"), html.P("Employee Weight")],
                         id = "weight", className = "mini-container",
                    style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
                 html.Br(),
                 html.Br(),
                 
            html.Div([html.H5(id = "Absent hours"), html.P("Absentism Hours")],
                    id = "No of hrs off work", className = "mini-container",
                    style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
            
        ], width = 2),
        
        #Education and  Disciplinary Failure
        dbc.Col([html.Div([html.H5(id = "Education"), html.P("Current Education")],
                         id = "Educ", className = "mini-container",
                    style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
                 html.Br(),
                 html.Br(),
                 
            html.Div([html.H5(id = "Discipline"), html.P("Disciplinary Failure")],
                    id = "Disc", className = "mini-container",
                    style = {'box-shadow': '0px 1px 3px rgba(0,0,0,.35)',
                        "border-radius": "5px",
                        "background-color": "#f9f9f9",
                        "margin": "7px",
                        "padding": "15px",
                        "position": "relative",
                        "text-align": "center"}),
            
        ], width = 2),
            
        ])
        
    ]),
    
    html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by Employment date:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=2011,
                            max=2016,
                            value=[2012, 2013],
                            className="dcc_control",
                        ),
                        html.P("Filter by Employee status:", className="control_label"),
                        dcc.RadioItems(
                            id="emp_status_selector",
                            options=[
                                {"label": "All", "value" : ["HIRED", "SEPARATED", "UPDATED"]},
                                {"label": "Hired ", "value": ["HIRED"]},
                                {"label": "Separated ", "value": ["SEPARATED"]},
                                {"label": "Updated ", "value": ["UPDATED"]}
                            ],
                            value=["HIRED"],
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ), html.Br(),
                        html.P(
                            "Chose a Region:",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="Region",
                            options=[
                                     {"label" : "United States", "value" : "US"},
                                     {"label" : "Asia-Pacific", "value" : "APAC"},
                                     {"label" : "Europe", "value" : "EMEA"}
                            ],
                            multi=True,
                            value=["US", "APAC"],
                            className="dcc_control"
                        ), html.P(
                            "Chose a Business Function:",
                            className="control_label",
                        ),
                         dcc.Dropdown(
                            id="Business Function",
                            options=[
                                     {"label" : "Corporate", "value" : "Corporate"},
                                     {"label" : "Development", "value" : "Development"},
                                     {"label" : "Operations", "value" : "Operations"},
                                     {"label" : "Sales", "value" : "Sales"},
                                     {"label" : "Marketing", "value" : "Marketing"}
                            ],
                            multi=True,
                            value=["Corporate", "Development"],
                            className="dcc_control"
                        )
                        
                    ],
                     style = {"border-radius": "5px",
                      "background-color": "#f9f9f9",
                      "margin": "10px",
                      "height" : "470px",
                      "margin-left" : "31px",
                      "padding": "25px",
                      "box-shadow": "0px 1px 3px rgba(0,0,0,.35)",
                             "width" : "23.3%",
                             "display" : "inline-block"}
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns"
                , style = {"border-radius": "5px",
                           "display" : "inline-block",
                           "float": "right",
                           "margin-right": "130px",
                           "margin-top": "10px",
                            "padding": "10px",
                           "box-shadow": "0px 1px 3px rgba(0,0,0,.35)",
                           "width" : "63.5%",
                           "display" : "inline-block",
                           "backgroundColor" : "#f9f9f9"
                          })
                  ]),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div(
                    [dcc.Graph(id="JobFamily")],
                    className="pretty_container five columns"
                , style = {"border-radius": "10px",
                      "background-color": "#f9f9f9",
                      #"padding": "10px",
                      "margin": "10px",
                      "margin-left" : "31px",
                      "box-shadow": "0px 1px 3px rgba(0,0,0,.35)",
                             "width" : "50%",
                             "display" : "inline-block"
                          }),
        
        html.Div(
                    [dcc.Graph(id="JobLevel")],
                    className="pretty_container five columns"
                , style = {"border-radius": "10px",
                           "display" : "inline-block",
                           "float": "right",
                           #"padding": "10px",
                           "margin-right": "130px",
                           "margin-top": "10px",
                           "box-shadow": "0px 1px 3px rgba(0,0,0,.35)",
                           "width" : "35%",
                           "display" : "inline-block"
                          })
    
    
    
    
    
    ])
])

##########App callback
@app.callback(
    Output(component_id = "out", component_property = "children"),
    [Input(component_id = "Input_Id", component_property = "value")])


def update(Id):
    return 'You\'ve entered "{}"'.format(Id)

@app.callback(
    [Output(component_id = "Absentee_guage", component_property = "children"),
     Output(component_id = "Emp Age", component_property = "children"),
     Output(component_id = "Emp Height", component_property = "children"),
     Output(component_id = "Emp Distance", component_property = "children"),
     Output(component_id = "Emp Weight", component_property = "children"),
     Output(component_id = "Absent hours", component_property = "children"),
     Output(component_id = "Education", component_property = "children"),
     Output(component_id = "Discipline", component_property = "children")],
    [Input(component_id = "Input_Id", component_property = "value")])


def update_guage(Id):
    dff = df2.copy()
    
    #get the average age
    #Avg_age = round(dff["Age"].mean())
    
    #build KPI guage for age
    #first get how many times any employee has been absent
    #emp_abs = len(dff[dff["ID"] == 30])
    
    #get the average absent numbers
    #avg_abs = absence(df)
    
    #return absent days
    if Id is None:
        abs_ = absence(df) #average absent days
        age_emp = str(round(df["Age"].mean())) + " " + "[Avg Age]" #average age
        height = round(df["Height"].mean()) #average height
        avg_distance = str(round(df["Distance from Residence to Work"].mean())) + " " + "Km"  #employee distance from work
        weight = str(round(df["Weight"].mean()))  + " " +"Pounds"
        abste = str(round(df["Absenteeism time in hours"].mean())) + " " + "Hours"
        education = "Education"
        discipline = "Yes/No"
    else:
        abs_ = len(dff[dff["ID"] == int(Id)])
        #Extract current age for any employee
        emp_info =  dff[dff["ID"] == int(Id)]
        #current age
        age_emp = emp_info["Age"].max()
        
        #Extract current height
        height = emp_info["Height"].max()
        
        #Extract avg distance from work
        avg_distance = str(emp_info["Distance from Residence to Work"].max()) + " " + "Km"
        
        #Extract weight
        weight = str(emp_info["Weight"].max()) + " " + "Pounds"
        
        #absent hours
        abste = str(sum(emp_info["Absenteeism time in hours"])) + " " + "Hours"
        
        #education level
        education = emp_info.iloc[0, 12]
        
        #discipline
        discipline = emp_info.iloc[0, 11]
    #return current employee age
    return abs_, age_emp, height, avg_distance, weight, abste, education, discipline


#organzational overview callback
@app.callback(
      Output(component_id = "individual_graph", component_property = "figure"),
    [Input(component_id = "year_slider", component_property = "value"),
     Input(component_id = "emp_status_selector", component_property = "value"),
     Input(component_id = "Region", component_property = "value"),
     Input(component_id = "Business Function", component_property = "value")]
)

def update_graph(year, status, region, function):
    
    
    #colors = ["#7FDBFF" if i not in year else "#0074D9"
     #         for i in range(year[0], year[1])]
    
    
    #add the year callback
    hr_new = hr.copy()
    year = list(year)
    a = int(year[0])
    b = int(year[1])
    hr_new = hr_new[hr_new["Year"].between(a, b)]
    
    ##specificy bar graph color

    hr_new = hr.copy()
    year = list(year)
    a = int(year[0])
    b = int(year[1])
    
   # stats = []
    
    #regs = []
    
    #for i in status:
      #  stats.append(var)
    
    #for i in region:
     #   regs.append(i)
    
    
    hr_new = hr_new[hr_new["Year"].between(a, b)]
    
    hr_new = hr_new[hr_new["HR Event"].isin(status)]
    
    hr_new = hr_new[hr_new["Region"].isin(region)]
    
    hr_new = hr_new[hr_new["Business Function"].isin(function)]
    
    hr_new['month_year'] = pd.to_datetime(hr_new['Date']).dt.to_period('M')

    hr_dt = hr_new.groupby(["month_year", "Region"]).size().reset_index()

    hr_dt.columns = ["MonthYear", "Region", "Count"]
    hr_dt

    #pd.to_datetime(hr_dt["MonthYear"])

    hr_dt['MonthYear'].dt.to_timestamp('s').dt.strftime('%Y-%m-%d')

    fig = px.bar(hr_dt, x=hr_dt['MonthYear'].dt.to_timestamp('s').dt.strftime('%Y-%m-%d'), y="Count",
                color = "Region", barmode = "group", text = "Count", title = "Employee Count")
    template = "simple_white"
    #change background color
    fig.layout.plot_bgcolor = '#f9f9f9'
    
    #update layout
    fig.update_layout(template = template)
    #fig.update_traces(marker_color = colors)
    
    
    #education stats
    
    return fig


@app.callback(
    [Output(component_id = "JobFamily", component_property = "figure"),
     Output(component_id = "JobLevel", component_property = "figure")],
    [Input(component_id = "year_slider", component_property = "value"),
     Input(component_id = "emp_status_selector", component_property = "value"),
     Input(component_id = "Region", component_property = "value"),
     Input(component_id = "Business Function", component_property = "value")]
)

def update_graph2(year, status, region, function):
    hr_new = hr.copy()
    year = list(year)
    a = int(year[0])
    b = int(year[1])
    
   # stats = []
    
    #regs = []
    
    #for i in status:
      #  stats.append(var)
    
    #for i in region:
     #   regs.append(i)
    
    
    hr_new = hr_new[hr_new["Year"].between(a, b)]
    
    hr_new = hr_new[hr_new["HR Event"].isin(status)]
    
    hr_new = hr_new[hr_new["Region"].isin(region)]
    
    hr_new = hr_new[hr_new["Business Function"].isin(function)]
    
    Job = hr_new.groupby(["Job Family", "Job Level"]).size().reset_index()

    Job.columns = ['Job Family', "Job Level", "Count"]

    fig2 = px.bar(Job, x = "Job Family", y = "Count", title = "Job Families", text = "Count",
                 color = "Job Level")
    
    fig3 = px.pie(Job, names = "Job Level", values = "Count", title = "Job Levels")
    
    #legend layout fig2
    fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))
    
    #legend layout fig 3
    fig3.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1.2
    ))
    fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
    return fig2, fig3


#@app.callback(
 #    Output(component_id = "plotly-image", component_property = "children"),
  #  [Input(component_id = "Input_Id", component_property = "value")]

#)
    
    
    
if __name__ == '__main__':
    app.run_server()


# In[11]:


print(dbc.__version__)

