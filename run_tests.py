import unittest,inspect

def passingStr(*args,backs=1):
    level = inspect.currentframe()
    for i in range(backs):
        level = level.f_back
    print(f"\033[32mPassing {level.f_code.co_name}!",*args,"\033[0m")

import E6Api as api

# exampleApiPosts = {'posts': [{'id': 6670468, 'created_at': '2026-08-31T13:10:04.954-04:00', 'updated_at': '2026-08-31T13:16:54.710-04:00', 'file': {'width': 2000, 'height': 2000, 'ext': 'png', 'size': 3551698, 'md5': '98a7f7d9c89e2ffa7895650c86cbfae3', 'url': 'https://static1.e621.net/data/98/a7/98a7f7d9c89e2ffa7895650c86cbfae3.png'}, 'preview': {'width': 256, 'height': 256, 'url': 'https://static1.e621.net/data/preview/98/a7/98a7f7d9c89e2ffa7895650c86cbfae3.jpg', 'alt': 'https://static1.e621.net/data/preview/98/a7/98a7f7d9c89e2ffa7895650c86cbfae3.webp'}, 'sample': {'has': True, 'width': 850, 'height': 850, 'url': 'https://static1.e621.net/data/sample/98/a7/98a7f7d9c89e2ffa7895650c86cbfae3.jpg', 'alt': 'https://static1.e621.net/data/sample/98/a7/98a7f7d9c89e2ffa7895650c86cbfae3.webp', 'alternates': {}}, 'score': {'up': 1, 'down': 0, 'total': 1}, 'tags': {'general': ['anthro', 'bare_shoulders', 'beak', 'black_beak', 'claws', 'clothing', 'dress', 'feathers', 'female', 'grass', 'grey_body', 'grey_feathers', 'holding_clothing', 'holding_dress', 'holding_object', 'looking_at_viewer', 'multicolored_beak', 'open_beak', 'open_mouth', 'orange_body', 'orange_feathers', 'plant', 'simple_background', 'solo', 'tall_grass', 'talon_hands', 'tan_beak', 'yellow_clothing', 'yellow_dress', 'yellow_talons'], 'artist': ['junoravenn'], 'contributor': [], 'copyright': [], 'character': ['juliette_(junoravenn)'], 'species': ['accipitrid', 'accipitriform', 'african_harrier-hawk', 'avian', 'bird'], 'invalid': [], 'meta': ['1:1', 'hi_res', 'signature'], 'lore': []}, 'locked_tags': [], 'change_seq': 79002927, 'flags': {'pending': True, 'flagged': False, 'note_locked': False, 'status_locked': False, 'rating_locked': False, 'deleted': False}, 'rating': 's', 'fav_count': 1, 'sources': ['https://bsky.app/profile/did:plc:dnppudgiitqp3bytxz45vpsp/post/3mgnk4zzru22x', 'https://www.furaffinity.net/view/64268493/', 'https://www.deviantart.com/junoravenn/art/African-harrier-hawk-1307883803'], 'pools': [], 'relationships': {'parent_id': None, 'has_children': False, 'has_active_children': False, 'children': []}, 'approver_id': None, 'uploader_id': 2120951, 'uploader_name': 'ElectroTiel', 'description': '', 'comment_count': 0, 'is_favorited': False, 'vote': 0, 'has_notes': False, 'duration': None}, {'id': 6670466, 'created_at': '2026-08-31T13:10:01.302-04:00', 'updated_at': '2026-08-31T13:10:01.302-04:00', 'file': {'width': 838, 'height': 549, 'ext': 'jpg', 'size': 202829, 'md5': '6ff840e634fe05965ea24ab11b070314', 'url': 'https://static1.e621.net/data/6f/f8/6ff840e634fe05965ea24ab11b070314.jpg'}, 'preview': {'width': 391, 'height': 256, 'url': 'https://static1.e621.net/data/preview/6f/f8/6ff840e634fe05965ea24ab11b070314.jpg', 'alt': 'https://static1.e621.net/data/preview/6f/f8/6ff840e634fe05965ea24ab11b070314.webp'}, 'sample': {'has': False, 'width': 838, 'height': 549, 'url': None, 'alt': None, 'alternates': {}}, 'score': {'up': 1, 'down': 0, 'total': 1}, 'tags': {'general': ['3_toes', '4_fingers', 'anthro', 'bill_(anatomy)', 'black_body', 'black_clothing', 'black_feathers', 'black_jacket', 'black_topwear', 'blonde_hair', 'bottomwear', 'breasts', 'brown_bottomwear', 'brown_clothing', 'brown_pants', 'buckteeth', 'carrot', 'chibi', 'cleavage', 'clothed', 'clothing', 'eyebrows', 'feathers', 'featureless_crotch', 'feet', 'female', 'fingers', 'food', 'fur', 'gloves', 'gloves_only', 'grey_body', 'grey_fur', 'group', 'hair', 'handwear', 'handwear_only', 'holding_carrot', 'holding_food', 'holding_object', 'holding_vegetable', 'jacket', 'male', 'mostly_nude', 'nude_anthro', 'nude_male', 'open_mouth', 'open_smile', 'orange_bill', 'orange_body', 'orange_fur', 'pants', 'plant', 'ponytail_ears', 'raised_eyebrow', 'scut_tail', 'scuted_legs', 'scutes', 'shirt', 'short_tail', 'smile', 'standing', 'tail', 'tail_feathers', 'tank_top', 'teeth', 'toes', 'topwear', 'trio', 'vegetable', 'white_clothing', 'white_gloves', 'white_handwear', 'wide_hipped_anthro', 'wide_hipped_male', 'wide_hips', 'yellow_clothing', 'yellow_shirt', 'yellow_tank_top', 'yellow_topwear'], 'artist': ['bigdad'], 'contributor': [], 'copyright': ['looney_tunes', 'warner_brothers'], 'character': ['bugs_bunny', 'daffy_duck', 'lola_bunny'], 'species': ['anatid', 'anseriform', 'avian', 'bird', 'duck', 'lagomorph', 'leporid', 'mammal', 'rabbit'], 'invalid': [], 'meta': ['2026'], 'lore': []}, 'locked_tags': [], 'change_seq': 79002620, 'flags': {'pending': False, 'flagged': False, 'note_locked': False, 'status_locked': False, 'rating_locked': False, 'deleted': False}, 'rating': 's', 'fav_count': 0, 'sources': ['https://www.furaffinity.net/view/66211094/'], 'pools': [], 'relationships': {'parent_id': None, 'has_children': False, 'has_active_children': False, 'children': []}, 'approver_id': None, 'uploader_id': 1618425, 'uploader_name': 'Alex64', 'description': '', 'comment_count': 0, 'is_favorited': False, 'vote': 0, 'has_notes': False, 'duration': None}, {'id': 6670458, 'created_at': '2026-08-31T13:06:07.783-04:00', 'updated_at': '2026-08-31T13:06:12.256-04:00', 'file': {'width': 1500, 'height': 3000, 'ext': 'jpg', 'size': 5038828, 'md5': '5ca9a4fede822565f270b64ff96c7362', 'url': 'https://static1.e621.net/data/5c/a9/5ca9a4fede822565f270b64ff96c7362.jpg'}, 'preview': {'width': 256, 'height': 512, 'url': 'https://static1.e621.net/data/preview/5c/a9/5ca9a4fede822565f270b64ff96c7362.jpg', 'alt': 'https://static1.e621.net/data/preview/5c/a9/5ca9a4fede822565f270b64ff96c7362.webp'}, 'sample': {'has': True, 'width': 850, 'height': 1700, 'url': 'https://static1.e621.net/data/sample/5c/a9/5ca9a4fede822565f270b64ff96c7362.jpg', 'alt': 'https://static1.e621.net/data/sample/5c/a9/5ca9a4fede822565f270b64ff96c7362.webp', 'alternates': {}}, 'score': {'up': 1, 'down': 0, 'total': 1}, 'tags': {'general': ['blue_hair', 'choker', 'clothed', 'clothed_female', 'clothed_humanoid', 'clothing', 'cloud', 'colored_nails', 'dress', 'evening', 'female', 'female_humanoid', 'fingernails', 'frilly', 'frilly_clothing', 'frilly_dress', 'hair', 'humanoid_pointy_ears', 'jewelry', 'long_fingernails', 'membrane_(anatomy)', 'membranous_wings', 'mountain', 'nails', 'necklace', 'pink_clothing', 'pink_dress', 'pointy_ears', 'red_choker', 'red_eyes', 'red_fingernails', 'red_jewelry', 'red_nails', 'red_necklace', 'sitting', 'solo', 'wings'], 'artist': ['banjie_(artist)'], 'contributor': [], 'copyright': ['touhou'], 'character': ['remilia_scarlet'], 'species': ['humanoid', 'vampire', 'winged_humanoid'], 'invalid': [], 'meta': ['1:2', 'absurd_res', 'film_grain', 'hi_res'], 'lore': []}, 'locked_tags': [], 'change_seq': 79002401, 'flags': {'pending': False, 'flagged': False, 'note_locked': False, 'status_locked': False, 'rating_locked': False, 'deleted': False}, 'rating': 's', 'fav_count': 1, 'sources': ['https://www.pixiv.net/artworks/146992051', 'https://i.pximg.net/img-original/img/2026/07/09/10/57/57/146992051_p0.jpg', 'https://danbooru.donmai.us/posts/11755037'], 'pools': [], 'relationships': {'parent_id': None, 'has_children': False, 'has_active_children': False, 'children': []}, 'approver_id': None, 'uploader_id': 202019, 'uploader_name': 'FluxUmbreon115', 'description': '', 'comment_count': 0, 'is_favorited': False, 'vote': 0, 'has_notes': False, 'duration': None}, {'id': 6670452, 'created_at': '2026-08-31T13:01:47.462-04:00', 'updated_at': '2026-08-31T13:13:05.894-04:00', 'file': {'width': 3600, 'height': 3600, 'ext': 'jpg', 'size': 1410810, 'md5': '5acb1dbdb258d8a5be9a19b060fe3dca', 'url': 'https://static1.e621.net/data/5a/cb/5acb1dbdb258d8a5be9a19b060fe3dca.jpg'}, 'preview': {'width': 256, 'height': 256, 'url': 'https://static1.e621.net/data/preview/5a/cb/5acb1dbdb258d8a5be9a19b060fe3dca.jpg', 'alt': 'https://static1.e621.net/data/preview/5a/cb/5acb1dbdb258d8a5be9a19b060fe3dca.webp'}, 'sample': {'has': True, 'width': 850, 'height': 850, 'url': 'https://static1.e621.net/data/sample/5a/cb/5acb1dbdb258d8a5be9a19b060fe3dca.jpg', 'alt': 'https://static1.e621.net/data/sample/5a/cb/5acb1dbdb258d8a5be9a19b060fe3dca.webp', 'alternates': {}}, 'score': {'up': 0, 'down': 0, 'total': 0}, 'tags': {'general': ['action_scene', 'anthro', 'attack', 'axe', 'brown_body', 'brown_fur', 'feet', 'female', 'fur', 'gauntlet_(weapon)', 'group', 'male', 'shield', 'smile', 'tongue', 'yellow_eyes'], 'artist': ['ceehaz'], 'contributor': [], 'copyright': ['dog_knight_rpg'], 'character': ['maci_(ceehaz)', 'nix_(ceehaz)'], 'species': ['canid', 'canine', 'canis', 'domestic_dog', 'hyena', 'mammal'], 'invalid': [], 'meta': ['absurd_res', 'hi_res'], 'lore': []}, 'locked_tags': [], 'change_seq': 79002189, 'flags': {'pending': False, 'flagged': False, 'note_locked': False, 'status_locked': False, 'rating_locked': False, 'deleted': False}, 'rating': 's', 'fav_count': 1, 'sources': ['https://x.com/CeeHaz/status/2094463254160687454'], 'pools': [], 'relationships': {'parent_id': None, 'has_children': False, 'has_active_children': False, 'children': []}, 'approver_id': None, 'uploader_id': 45812, 'uploader_name': 'The_Panda', 'description': '', 'comment_count': 0, 'is_favorited': False, 'vote': 0, 'has_notes': False, 'duration': None}]}
exampleApiPosts = api.search(["ails"],limit=4)[1]

class TestTagMatches(unittest.TestCase):
    def tagCheck(self,debug,tags,condition,passpost=False,customDebugPrint=None):
        import TagMatches
        name = inspect.currentframe().f_back.f_code.co_name
        if debug: print(f"---------- Started test {name}")
        for post in exampleApiPosts["posts"]:
            match = TagMatches.matchTags(post,tags)
            alltags = TagMatches.getAllTags(post)
            cond = condition(post if passpost else alltags)
            if debug: print(match,cond,alltags,customDebugPrint(post) if customDebugPrint else "","\n")
            self.assertEqual(match,cond)
    def test_nomale(self):
        self.tagCheck(False,["-male"],lambda x : not "male" in x)
    def test_yesmale(self):
        self.tagCheck(False,["male"],lambda x : "male" in x)
    def test_nomaleorfemale(self):
        self.tagCheck(False,["-male","-female"],lambda x : (not "male" in x) and (not "female" in x))
    def test_maleorfemale(self):
        self.tagCheck(False,["~male","~female"],lambda x : ("male" in x) or ("female" in x))
    def test_maleandfemale(self):
        self.tagCheck(False,["male","female"],lambda x : ("male" in x) and ("female" in x))
    def test_safe(self):
        self.tagCheck(False,["rating:s"],lambda x : x["rating"] == "s",True)
    def test_questionable(self):
        self.tagCheck(False,["rating:q"],lambda x : x["rating"] == "q",True)
    def test_explicit(self):
        self.tagCheck(False,["rating:e"],lambda x : x["rating"] == "e",True)
    def test_explicitalias(self):
        self.tagCheck(False,["rating:x"],lambda x : x["rating"] == "e",True)
    def test_unsafe(self):
        self.tagCheck(False,["-rating:s"],lambda x : not x["rating"] == "s",True)
    def test_filesizerange1(self):
        self.tagCheck(False,["filesize:200KB..400KB"],lambda x : x["file"]["size"] >= 200*1024 and x["file"]["size"] <= 400*1024,True)
    def test_filesizerange2(self):
        self.tagCheck(False,["filesize:200KB..800KB"],lambda x : x["file"]["size"] >= 200*1024 and x["file"]["size"] <= 800*1024,True)
    def test_filesizerange3(self):
        self.tagCheck(False,["filesize:200KB..1MB"],lambda x : x["file"]["size"] >= 200*1024 and x["file"]["size"] <= 1024*1024,True)
    def test_filesizerange4(self):
        self.tagCheck(False,["filesize:100KB..200KB"],lambda x : x["file"]["size"] >= 100*1024 and x["file"]["size"] <= 200*1024,True)
    def test_widthrange1(self):
        self.tagCheck(False,["width:>=250"],lambda x : x["file"]["width"] >= 250,True)
    def test_widthrange2(self):
        self.tagCheck(False,["width:>=500"],lambda x : x["file"]["width"] >= 500,True)
    def test_widthrange3(self):
        self.tagCheck(False,["width:>=750"],lambda x : x["file"]["width"] >= 750,True)
    def test_widthrange4(self):
        self.tagCheck(False,["width:>=1000"],lambda x : x["file"]["width"] >= 1000,True)
    def test_heightrange1(self):
        self.tagCheck(False,["height:<=250"],lambda x : x["file"]["height"] <= 250,True)
    def test_heightrange2(self):
        self.tagCheck(False,["height:<=500"],lambda x : x["file"]["height"] <= 500,True)
    def test_heightrange3(self):
        self.tagCheck(False,["height:<=750"],lambda x : x["file"]["height"] <= 750,True)
    def test_heightrange4(self):
        self.tagCheck(False,["height:<=1000"],lambda x : x["file"]["height"] <= 1000,True,customDebugPrint=lambda x : x["file"]["height"])
    def test_heightrange4(self):
        self.tagCheck(False,["height:<=1000"],lambda x : x["file"]["height"] <= 1000,True,customDebugPrint=lambda x : x["file"]["height"])
    def test_hasparent(self):
        self.tagCheck(False,["hasparent:yes"],lambda x : x["relationships"]["parent_id"] != 0,True,customDebugPrint=lambda x : x["file"]["height"])
    def test_ischild(self):
        self.tagCheck(False,["ischild:true"],lambda x : x["relationships"]["parent_id"] != 0,True,customDebugPrint=lambda x : x["file"]["height"])
    def test_isparent(self):
        self.tagCheck(False,["isparent:true"],lambda x : x["relationships"]["has_children"],True,customDebugPrint=lambda x : x["file"]["height"])
    def test_haschild(self):
        self.tagCheck(False,["haschild:true"],lambda x : x["relationships"]["has_children"],True,customDebugPrint=lambda x : x["file"]["height"])


class TestDText(unittest.TestCase):
    def render_equal(self,torender,equal):
        import DText
        rendered = DText.renderDText(torender)
        self.assertEqual(rendered,equal)
        passingStr(rendered,backs=2)
    def test_renderBISU(self):
        self.render_equal("[b]b[/b][i]i[/i][s]s[/s][u]u[/u][b][i][s]`[u]bisu[/u]`[/s][/i][/b]","§b§b§i§i§s§s§u§u§bis§`[u]bisu[/u]`")
    def test_renderColor(self):
        self.render_equal("[color=red]test[/color]","§31§test")
    def test_renderColorNest(self):
        self.render_equal("[color=red]test[color=lime]test[/color]test[/color]","§31§test§32§test§31§test")
    def test_renderSpoiler(self):
        self.render_equal("[spoiler]test[/spoiler]","§90;100§test")
    def test_renderQuote(self):
        self.render_equal("[quote]test[/quote]test","\n§107d§  test\n§§test")

class TestColoredString(unittest.TestCase):
    def test_generics(self):
        from ColoredString import CString
        from TermUtils import printw
        printw(CString("§90;100§test"),"from [spoiler]test[/spoiler]")
        printw(CString("§b§b§i§i§s§s§u§u§bis§`[u]bisu[/u]`"),"from [b]b[/b][i]i[/i][s]s[/s][u]u[/u][b][i][s]`[u]bisu[/u]`[/s][/i][/b]")
        printw(CString("§31§test"),"from [color=red]test[/color]")
        printw(CString("§31§test§32§test§31§test"),"from [color=red]test[color=lime]test[/color]test[/color]")
        printw("testing one two three four five six pneumonoultramicroscopicsilicovolcanoconiosis",wrapLen=10)
        printw("8/17付デイリーランキング20位、8/17～8/23付ウィークリーランキング19位でした！閲覧＆評価＆ブクマ、ありがとうございます！",wrapLen=10)
        print("1234567890123456789012345678901234567890")
if __name__ == "__main__":
    unittest.main()