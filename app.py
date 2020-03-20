from flask import Flask, request, jsonify

import chatbot.chatbot as chatbot
import graphs.graphs as graphs
import sentiments.sentiments as sentiments
import tweets.tweets as tweets



app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def predict():
    message = "hello"
    print(request.args.get('message'))
    message = request.args.get('message')
    intents = chat_bot.predict_class(message, chat_bot.model)
    res = chat_bot.getResponse(intents)
    print(res)
    return jsonify(res)
    #return "Cool!"
#todo: sort monthly data
@app.route("/metrics", methods=["GET","POST"])
def get_tweet_metrics():
    print(request.args)
    scope = request.args.get('scope')
    print(scope)

    if scope == "day":
        return jsonify(t_graph.get_daily_metrics())
    elif scope == "month":
        return jsonify(t_graph.get_monthly_metrics())
    else:
        return jsonify(t_graph.get_yearly_metrics())

@app.route("/tweets",methods=["GET","POST"])
def get_tweets():
    data = t_tweets.get_recent_tweets(5)
    return data

@app.route("/polarity", methods=["GET"])
def get_polarity():
    data = t_sentis.get_polarity()
    return data

if __name__ == "__main__":
    #Init all the ML Models
    global chat_bot, t_graph, t_tweets, t_sentis
    chat_bot = chatbot.Chatbot(app)
    t_graph = graphs.Graphs(app)
    t_tweets = tweets.Tweets(app)
    t_sentis = sentiments.Sentiments(app)
    #Have a config file for ports and static stuff
    app.run()