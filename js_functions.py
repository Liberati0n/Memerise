class Functions:
    # Small organisation
    def __init__(self):
        self.get_english = """
        words = []
        document.querySelectorAll("#content > div > div > div.things.clearfix > div > div.col_b.col.text > div").forEach(function(word) {
            words.push(word.innerText)
        })
        return words"""
        self.get_foreign = """
        words = []
        document.querySelectorAll("#content > div > div > div.things.clearfix > div > div.col_a.col.text > div").forEach(function(word) {
            words.push(word.innerText)
        })
        return words"""
        self.next_slide = "document.querySelector('.next-button').click()"
        self.is_text = """
        if (document.querySelector('#boxes > div > div.mem-area.show-want-mem > div.want-mem.cnt > a')) {
            return true;
        }
        return false;"""
        self.is_multi_choice = """
        if (document.querySelector("#boxes > div > ol > li:nth-child(1)")) {
            return true;
        } 
        return false;"""
        self.is_type = """
        if (document.querySelector("#boxes > div > div.typing-wrapper > input")) {
            return true;
        } 
        return false;"""
        self.is_dumb = """
        if (document.querySelector(".word-box-response")) {
            return true;
        } 
        return false;"""
        self.is_done = """
        if (document.querySelector("#session-complete-banner > p:nth-child(1)")) {
            return true;
        } 
        return false;"""
        self.is_broke = """
        if (document.querySelector("div.modal-body:nth-child(2)")) {
            return true;
        } 
        return false;
        """

    @staticmethod
    def get_button_by_text(text):
        return """
            function findButtonByText(text) {
                buttons = document.querySelectorAll("#boxes > div > ol > li > .val")
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].innerText == text) {
                        return i;
                    }
                }
                return -1;
            }
            """ + "return findButtonByText(`" + text + "`)"
