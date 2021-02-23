html.H1(children='Seattle Crime Dashboard'),

    html.Div(children='''
        Map: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    

    html.Div(children='''
        Person Offenses within the Date and Radius Specified
    '''),
    html.Div(children='''
        Property Offenses within the Date and Radius Specified
    '''),
    html.Div(children='''
        Society Offenses within the Date and Radius Specified
    '''),