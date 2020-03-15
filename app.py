from flask import Flask, request, jsonify

import chatbot.chatbot as chatbot
import graphs.graphs as graphs
import sentiments.sentiments as sentiments
import tweets.tweets as tweets



app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def predict():
    message = "hello"
    #print(request.args.get('message'))
    message = request.args.get('message')
    intents = chat_bot.predict_class(message, chat_bot.model)
    #res = chatbot.getResponse(intents, intents)
    #print(res)
    #return jsonify(res)
    return "Cool!"

@app.route("/metrics", methods=["GET","POST"])
def get_tweet_metrics():
    print(request.args)
    scope = request.args.get('scope')
    print(scope)
    data = None
    if scope == "day":
        data = t_graph.get_daily_metrics()
    elif scope == "month":
        data = t_graph.get_monthly_metrics()
    else:
        data = t_graph.get_yearly_metrics()
    return data

@app.route("/graphData",methods=["GET","POST"])
def get_graphData():
    pass

@app.route("/tweets",methods=["GET","POST"])
def get_tweets():
    data = t_tweets.get_recent_tweets(10)
    return data


if __name__ == "__main__":
    #Init all the ML Models
    global chat_bot, t_graph, t_tweets
    chat_bot = chatbot.Chatbot(app)
    t_graph = graphs.Graphs(app)
    t_tweets = tweets.Tweets(app)
    #Have a config file for ports and static stuff
    app.run()