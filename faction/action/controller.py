import faction.action.ui.action_ui


class ActionController:
    def __init__(self, cur_faction):
        self.faction = cur_faction
        self.ui = faction.action.ui.action_ui.ActionUI(self, self.faction.assets)

    def set_chosen_actor_asset(self, index):
        self.ui.populate_target_table(self.faction.assets[index].get_nearby_assets())
