import yaml
from character import Character
from world import World

class Story:
    def __init__(self, story):
        self.name = story
        self.load_story(story)

    def load_story(self, name):
        f = open('data/stories/%s/story.yaml' % name)
        data = yaml.load(f)
        f.close()
        self.world = World(data['world'])
        self.hero = Character('data/stories/%s' % name, data['hero'])
