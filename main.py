import yaml
import datetime

from topic import Topic
from game import Game


def game_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> Game:
    return Game(**loader.construct_mapping(node))

def topic_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> Topic:
    return Topic(**loader.construct_mapping(node))

def get_loader()->type[yaml.SafeLoader]:
    loader = yaml.SafeLoader
    loader.add_constructor('!Topic', topic_constructor)
    loader.add_constructor('!Game', game_constructor)
    return loader

def generate_html_from_topic(topic: Topic) -> str:
    out = "<div class='topic'>\n"
    out += f"<h2>{topic.Name()}</h2>\n"
    if topic.Date() != '':
        out += f"<p>Datum: {topic.Date()}</p>\n"
    out += f"<p>Moderator: {topic.Moderator()}</p>\n"
    for game in topic.Games(): #TOOD: get flag
        out += f"<p><a href='{game.Link()}'>{game.Name()}</a>, {game.Developer()}, {game.Plattform()}, ({game.Year()})</p>\n"
    out += "</div>\n"
    return out

def main():
    nextTopicId = '1'
    nextEveningDate = datetime.datetime(2026, 4, 9, 18, 0)
    
    nextTopic: Topic = Topic(-1, [], -1, -1, -1)
    openTopics = []
    pastTopics = []
    
    print("Compiler is running...")
    data = yaml.load(open("data.yaml", 'rb'), Loader=get_loader())
    print("Data loaded successfully!")
    
    for topic in data:
        print(f"Topic {topic.Id()}: {topic.Name()}, Date: {topic.Date()}")
    
    for topic in data:
        if topic.Id() == nextTopicId:
            nextTopic = topic
        elif topic.Date() == '':
            openTopics.append(topic)
        else:
            pastTopics.append(topic)
    
    if nextTopic.Id() == -1:
        print(f"Error: No topic with id {nextTopicId} found.")
        return
    
    content = ""
    
    content += "<h2>Nächster Termin</h2>\n"
    
    content += generate_html_from_topic(nextTopic)

    content += "<h2>Offene Themen</h2>\n"
    for topic in openTopics:
        content += generate_html_from_topic(topic)
    
    content += "<h2>Vergangene Themen</h2>\n"
    for topic in pastTopics:
        content += generate_html_from_topic(topic)
    
    with open("index.html", 'r') as file:
        html1 = file.read()
    with open("index.html.2", 'r') as file:
        html2 = file.read()
    
    output = html1 + content + html2
    with open("output/index.html", 'w') as file:
        file.write(output)

if __name__ == "__main__":
    main()