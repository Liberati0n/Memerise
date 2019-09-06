from selenium import webdriver
from js_functions import Functions
from time import sleep

course_url_base = "https://www.memrise.com/course/1137583/aqa-new-gcse-french-from-2016/{}"
num_modules = 39

driver = webdriver.Firefox()

functions = Functions()


def login():
    print("Opening login page...")
    driver.get("https://www.memrise.com/login/")
    input("Please login now. Press enter when done.")


def do_module(num):
    print("Doing module " + num)
    driver.get(course_url_base.format(num))
    print("Getting words...")
    english_words = driver.execute_script(functions.get_english)
    foreign_words = driver.execute_script(functions.get_foreign)
    print("Compiling word dictionaries...")
    english_to_foreign = {}
    for i in range(len(english_words)):
        english_to_foreign[english_words[i]] = foreign_words[i]
    foreign_to_english = {}
    for i in range(len(english_words)):
        foreign_to_english[foreign_words[i]] = english_words[i]
    print("[DBG] " + str(foreign_to_english) + "\n" + str(english_to_foreign))
    print("Doing slides...")
    module_done = False
    driver.get(course_url_base.format(num + "/garden/learn/"))
    sleep(1)  # Allow ample time for page load, possibly replace this with JS
    while not module_done:
        try:
            if driver.execute_script(functions.is_text):
                # Question is a text slide which we want to skip
                print("Slide is a definition page. Skipping.")
                driver.execute_script(functions.next_slide)

            elif driver.execute_script(functions.is_multi_choice):
                print("Finding multiple choice question...")
                # Question is a multi choice question, we should probably answer it.
                # Get question
                question = driver.execute_script(
                    'return document.querySelector("#prompt-row > div > div").innerText.trim()'
                )
                print("[DBG] " + question)
                # Find answer
                print("Finding answer...")
                try:
                    answer = english_to_foreign[question]
                except KeyError:
                    answer = foreign_to_english[question]
                print("[DBG] " + answer)
                print("Finding button...")
                print("Injecting JS to find button...")
                button_id = driver.execute_script(functions.get_button_by_text(answer))
                if button_id == -1:
                    driver.execute_script(functions.next_slide)
                    sleep(0.1)
                    driver.execute_script(functions.next_slide)
                    continue
                print(f"Found button ({button_id}). Clicking.")
                driver.execute_script("document.querySelector(`[data-choice-id='" + str(button_id) + "']`).click()")
                driver.execute_script(functions.next_slide)

            elif driver.execute_script(functions.is_type):
                print("Question is a typey question.")
                question = driver.execute_script(
                    'return document.querySelector("#prompt-row > div > div").innerText.trim()'
                )
                print("[DBG] " + question)
                # Find answer
                print("Finding answer...")
                try:
                    answer = english_to_foreign[question]
                except KeyError:
                    answer = foreign_to_english[question]
                print("Sending to input box")
                driver.find_element_by_css_selector(
                    "#boxes > div > div.typing-wrapper > input"
                ).send_keys(
                    answer + u'\ue007'
                )
                driver.execute_script(functions.next_slide)

            elif driver.execute_script(functions.is_dumb):
                print("Skipping question that is dumb and stupid")
                driver.execute_script(functions.next_slide)
                sleep(0.1)
                driver.execute_script(functions.next_slide)

            elif driver.execute_script(functions.is_done):
                return True

            elif driver.execute_script(functions.is_broke):
                return False
            print("Done. Next.")
            sleep(0.1)  # Allow page transitions
        except:
            try:
                driver.execute_script(functions.next_slide)
                sleep(0.1)
                driver.execute_script(functions.next_slide)
                sleep(0.1)
            except:
                return False





print("""
 _______ _______ _______ _______  ______ _____ _______ _______
 |  |  | |______ |  |  | |______ |_____/   |   |______ |______
 |  |  | |______ |  |  | |______ |    \_ __|__ ______| |______
                                                              
    -= Brought to you by your friends at Liberati0n =-
          -= Greetz to our friends at CD =-
""")

login()
for i in range(num_modules):
    do_module(str(i + 1))
input("Press any key to exit...")
driver.close()
