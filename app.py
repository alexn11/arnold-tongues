import flask
from matplotlib import colormaps

from TongueDrawer import TongueDrawer

app = flask.Flask(__name__, template_folder='templates')

def prepare_config(config: dict):
    prepared_config = {
        'family': '2x+T',
        'domain': {},
        'dynamics': {},
        'images': {
            'image_names': {
                'periods': '(streamed)',
            }
        },
        'misc': {
            'as_stream': True,
            'show_progress': True,
        }
    }
    if('family' in config):
        family = config['family']
        if(family in ['2x+T', '2x+S','dsm', '2xdsm']):
            prepared_config['family'] = family
    if('domain' in config):
        domain_config = config['domain']
        prepared_config['domain']['a_range'] = domain_config.get('a_range', (0., 1.))
        prepared_config['domain']['b_range'] = domain_config.get('b_range', (0., 1.))
    if('dynamics' in config):
        dyn_config = config['dynamics']
        prepared_config['dynamics']['default_starting_point'] = dyn_config.get('default_starting_point', 0.2142)
        prepared_config['dynamics']['nb_starting_points'] = dyn_config.get('nb_starting_points', 5)
        prepared_config['dynamics']['nb_initial_iterations'] =  dyn_config.get('nb_initial_iterations', 120)
        prepared_config['dynamics']['max_period'] = dyn_config.get('max_periods', 10)
        prepared_config['dynamics']['periodicity_tol'] = dyn_config.get('periodicity_tol', 1e-3)
    if('images' in config): 
        img_config = config['images']
        prepared_config['images']['width'] = img_config.get('width', 400)
        prepared_config['images']['height'] = img_config.get('height', 400)
        colour_map = img_config.get('colour_map')
        if((colour_map is None) or (colour_map not in colormaps())):
            colour_map = 'magma'
        prepared_config['images']['periods_colours'] = colour_map
    return prepared_config

def draw_the_tongues(config: dict):
    tongue_drawer = TongueDrawer(config['family'],
                                options_domain=config['domain'],
                                options_dynamics=config['dynamics'],
                                options_image=config['images'],
                                options_other=config['misc'])
    tongue_images = tongue_drawer.draw_the_tongues()
    return tongue_images

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/api/tongue', methods=['GET', 'POST'])
def tongue_api():
    print('reached api')
    config = prepare_config(flask.request.json)
    tongue_images = draw_the_tongues(config)
    return flask.send_file(tongue_images['periods'], mimetype='image/png')
