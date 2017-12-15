import pandas as pd
import io
import requests
import matplotlib as mpl
mpl.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, make_response
from library import clean_html, find_stats, np2t

# Connect newspaper logging to cloud
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
news_logger = logging.getLogger("newspaper")
client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
news_logger.addHandler(handler)

df = pd.read_json("stats.json")
rl_df = pd.read_json("real_stats.json")

app = Flask(__name__)


@app.route('/boxplot', methods = ["GET", "POST"])
def boxplot():
    ari = float(request.args.get("ari"))
    avg_word_len = float(request.args.get("avg_word_len"))
    avg_sent_len = float(request.args.get("avg_sent_len"))
    total_words = float(request.args.get("total_words"))
    total_sents = float(request.args.get("total_sents"))
    sentiment = float(request.args.get("sentiment"))
    fig = Figure()
    fig.set_size_inches(9, 12)

    fig.subplots_adjust(hspace = 0.5)

    axis = fig.add_subplot(6, 1, 1)
    axis.set_xlabel("ARI Score")
    axis.plot(ari, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.ari.values, vert = False) #real value
    axis.violinplot(df.ari.values, vert = False) #fake value

    axis = fig.add_subplot(6, 1, 2)
    axis.set_xlabel("Sentiment")
    axis.plot(sentiment, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.sentiment.values, vert = False)
    axis.violinplot(df.sentiment.values, vert = False)

    axis = fig.add_subplot(6, 1, 3)
    axis.set_xlabel("Mean Word Length")
    axis.plot(avg_word_len, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.avg_word_len.values, vert = False)
    axis.violinplot(df.avg_word_len.values, vert = False)

    axis = fig.add_subplot(6, 1, 4)
    axis.set_xlabel("Mean Sentence Length")
    axis.plot(avg_sent_len, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.avg_sent_len.values, vert = False)
    axis.violinplot(df.avg_sent_len.values, vert = False)

    axis = fig.add_subplot(6, 1, 5)
    axis.set_xlabel("Total Words")
    axis.plot(total_words, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.total_words.values, vert = False)
    axis.violinplot(df.total_words.values, vert = False)

    axis = fig.add_subplot(6, 1, 6)
    axis.set_xlabel("Total Sentences")
    axis.plot(total_sents, 1, "o", ms = 10, color = "red")
    axis.violinplot(rl_df.total_sents.values, vert = False)
    axis.violinplot(df.total_sents.values, vert = False)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response


@app.route('/graphs', methods = ["GET", "POST"])
def graphs():
    url = request.form["url"]
    text = request.form["text"]
    if url != "":
        text = np2t(url)

    stats = find_stats(text)

    stats_fmt = {}
    for k, v in stats.items():
        if type(v) is float:
            stats_fmt["fmt_" + k] = round(v, 1)
    stats.update(stats_fmt)
            
    bpq = "/boxplot?" + "&".join(["%s=%s" % (k, v) for k, v in stats.items()]) 
    
    return render_template("graphs.html", url = url, text = text[0:100], bpq=bpq, **stats)


@app.route('/query', methods = ["GET", "POST"])
def query():
    return render_template("query.html")


@app.route('/about', methods = ["GET", "POST"])
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug = True)
