from src import app


@app.template_filter('format_data')
def format_data(string):
    return string.replace('_', ' ').capitalize()

