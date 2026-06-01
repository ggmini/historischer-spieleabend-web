import yaml
import datetime
import shutil
import os

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
        d = topic.Date().date()
        out += f"<p>Datum: { str(d.day).rjust(2, '0')}.{str(d.month).rjust(2, '0')}.{d.year} 18:00</p>\n"
    out += f"<p class='mod'>Moderator*in: {topic.Moderator()}</p>\n"
    for game in topic.Games():
        country_code = game.Country().lower()
        country_html = ""
        if country_code != "":
            country_html = f'<span class="fi fi-{country_code}"></span>' 
        out += f"<p>{country_html}<a href='{game.Link()}'><i>{game.Name()}</i></a>, {game.Developer()}, {game.Plattform()} {game.Year()}.</p>\n"
    out += "</div>\n"
    return out

def main():
    nextTopicId = '6'
    
    nextTopic: Topic = Topic(-1, [], -1, "", -1)
    openTopics = []
    pastTopics = []
    
    print("Building website...")
    print("Loading data...")
    data = yaml.load(open("assets/data/data.yaml", 'rb'), Loader=get_loader())
    data_past = yaml.load(open("assets/data/data_past.yaml", 'rb'), Loader=get_loader())
    data_draft = yaml.load(open("assets/data/data_draft.yaml", 'rb'), Loader=get_loader())
    print("Data loaded successfully!")
    
    print("Processing data...")
    for topic in data:
        print(f"Topic {topic.Id()}: {topic.Name()}, Date: {topic.Date()}")
    for topic in data_past:
        print(f"Past Topic {topic.Id()}: {topic.Name()}, Date: {topic.Date()}")
    for topic in data_draft:
        print(f"Draft Topic {topic.Id()}: {topic.Name()}, Date: {topic.Date()}")
    
    for topic in data:
        if topic.Id() == nextTopicId:
            nextTopic = topic
        elif topic.Date() == '':
            openTopics.append(topic)
        else:
            pastTopics.append(topic)
    for topic in data_past:
        pastTopics.append(topic)

    pastTopics.sort(key=lambda t: t.Date(), reverse=True)

    if nextTopic.Id() == -1:
        print(f"Error: No topic with id {nextTopicId} found.")
        return
    
    content = ""    
    content += "<h2>Nächster Termin</h2>\n"
    content += generate_html_from_topic(nextTopic)

    content += "<h2>Offene Themen</h2>\n"
    content += "<div class='collection'>"
    for topic in openTopics:
        content += generate_html_from_topic(topic)
    content += "</div>\n"
    
    content += "<h2>Unfertige Themen</h2>\n"
    content += "<div class='collection'>"
    for topic in data_draft:
        content += generate_html_from_topic(topic)
    content += "</div>\n"

    content += "<h2>Vergangene Themen</h2>\n"
    content += "<div class='collection'>"
    for topic in pastTopics:
        content += generate_html_from_topic(topic)
    content += "</div>\n"

    print("Generating output...")    
    with open("assets/index.html", 'r') as file:
        html1 = file.read()
    with open("assets/index.html.2", 'r') as file:
        html2 = file.read()

    #Make output dir
    try:
        os.mkdir("output")
    except FileExistsError:
        pass
    #Copy CSS
    shutil.copy("assets/style.css", "output/style.css")
    
    #Create html
    output = html1 + content + html2
    with open("output/index.html", 'w') as file:
        file.write(output)
    print("Website built successfully!")
    
if __name__ == "__main__":
    main()