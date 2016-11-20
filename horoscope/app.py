from flask import Flask, render_template
app = Flask(__name__, static_folder='.')
from predict import load_frames, create_horoscope

from .image import jolanda

template = '''
<html>
    <head>
        <title>Bullshit generator</title>
    </head>

    <body>
        <h1>Nechte si predpovedet svou budoucnost!</h1>
        <p>
            {hrscp}
        </p>
        {img}
    </body>
    <style>
     body {{
         text-align: center;
        padding-left: 25%;
        padding-right: 25%;}}

h1 {{color: red;}}
    </style>
</html> '''

@app.route("/")
@app.route("/<int:size>")
def one_horoscope(size=None):
    if not size:
        size = 5
    if size > 10:
        return "max 10 pls :("
    # base = '/home/pocin/projects/engeto/horoscope/'
    # bigrams, first_words = load_frames(base+'bigrams_probs.csv',
    #                                    base+'first_world_probabilities.csv')
    bigrams, first_words = load_frames()
    horoscope = create_horoscope(size, first_words, bigrams)
    return template.format(hrscp=horoscope, img=jolanda)


if __name__ == "__main__":
    app.run()
