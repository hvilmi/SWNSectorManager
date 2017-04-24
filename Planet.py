class Planet:
    """description of class"""

    def __init__(self, name, pop, desc, tags, tl):
        self.name = name
        self.pop = pop
        self.desc = desc
        self.tags = tags
        self.tl = tl

    def get_name(self):
        return self.name

    def get_pop(self):
        return self.pop

    def get_tags(self):
        return self.tags

    def get_desc(self):
        return self.desc

    def get_tl(self):
        if self.tl:
            return int(self.tl)
        else:
            # No tech level set. Default to 0.
            return 0
    


        

