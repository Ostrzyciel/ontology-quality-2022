import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import json
import os

app = dash.Dash(
    __name__,
    external_stylesheets=['https://unpkg.com/purecss@2.0.6/build/pure-min.css']
)

data = json.load(open('../results/final_suspects.json'))

if os.path.isfile('../results/review_results.json'):
    results = json.load(open('../results/review_results.json'))
else:
    results = dict()

it = -1

app.layout = html.Div(
    className='pure-g',
    children=[
        html.Div(className='pure-u-1-1', id='label-top'),

        html.Div(
            dcc.Textarea(
                'textarea-comment',
                style={'width': '50%', 'height': 100},
            ),
            className='pure-u-1-1',
            style={'textAlign': 'center'}
        ),

        html.Div(
            children=[
                html.Button('Invalid', id='submit-invalid', className='pure-button button-error'),
                html.Button('Other issue', id='submit-other', className='pure-button button-secondary'),
                html.Button('Valid', id='submit-valid', className='pure-button button-success'),
            ],
            className='pure-u-1-1',
            style={'textAlign': 'center'}
        ),

        html.Div(html.Hr(), className='pure-u-1-1'),

        html.Div(dcc.Markdown(id='label-left'), className='pure-u-1-2'),
        html.Div(dcc.Markdown(id='label-right'), className='pure-u-1-2'),

        html.Div(
            html.Iframe(id='iframe-left', height='600px', width='100%', src=''),
            className='pure-u-1-2',
        ),
        html.Div(
            html.Iframe(id='iframe-right', height='600px', width='100%', src=''),
            className='pure-u-1-2',
        ),
    ]
)


@app.callback(
    Output('iframe-left', 'src'),
    Output('iframe-right', 'src'),
    Output('label-top', 'children'),
    Output('label-left', 'children'),
    Output('label-right', 'children'),
    Output('textarea-comment', 'value'),
    Input('submit-invalid', 'n_clicks'),
    Input('submit-other', 'n_clicks'),
    Input('submit-valid', 'n_clicks'),
    State('iframe-right', 'src'),
    State('textarea-comment', 'value'),
)
def show_next(n1, n2, n3, current_src, comment):
    if current_src != '':
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        results[current_src] = {
            'decision': button_id[7:],
            'comment': comment,
        }
        json.dump(results, open('../results/review_results.json', 'w'), indent=2)


    found = -1
    for i, row in enumerate(data):
        if row['dbpedia'] in results:
            pass
        else:
            found = i
            break

    if found == -1:
        return [
            '', '',
            'Finished.', '', '', ''
        ]

    return [
        data[found]['cso_topics'][0],
        data[found]['dbpedia'],
        f'Record: {found} / {len(data)}. Reason: {data[found]["reason"]}',
        '- ' + ('\n- '.join(data[found]['cso_topics'])),
        '- ' + data[found]['dbpedia'],
        '',
    ]


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
