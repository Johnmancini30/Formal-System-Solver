from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

USER_NAME = "johnbot"
URL = "http://michaelwehar.com/metatree/replacement/login.html"
path0 = "A_0-0"
path1 = "A_0-1"
path2 = "A_0-2"
n = .2 #sleep time
class Formal_System_Solver:

  def __init__(self, url):
    
    self.url = url
    self.browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
    sleep(n*10)

  def login(self):
    
    self.browser.get(self.url)
    username = self.browser.find_element_by_id("username")
    username.send_keys(USER_NAME)

    submit_button = self.browser.find_element_by_class_name('btn-success')
    submit_button.click()
    sleep(n)

  #only works on practice mode currently
  def play_game(self):

    while True:
      innerHTML = self.browser.execute_script("return document.body.innerHTML")
      soup = BeautifulSoup(innerHTML, 'html5lib')


      #getting initial string and final string
      div = soup.find("div", {"class":"well"})
      initial_word = div.find("span", {"id":"initialWord"}).text
      final_word = div.find("span", {"id":"finalWord"}).text

      #print(soup.prettify())
      
      #getting rules
      """
      We parse the html for the 3 lines that contain the rules, then split those lines by words. At that point we
      know the 3rd and 5th word of each line contains the 1st and seconds part of the rule respectively
      """
      rules = [div.find("a", {"id":path0}).text, div.find("a", {"id":path1}).text, div.find("a", {"id":path2}).text]
      rule0 = [rules[0].split(" ")[3][1:-1], rules[0].split(" ")[5][1:-1]]
      rule1 = [rules[1].split(" ")[3][1:-1], rules[1].split(" ")[5][1:-1]]
      rule2 = [rules[2].split(" ")[3][1:-1], rules[2].split(" ")[5][1:-1]]
      rules = [rule0, rule1, rule2]
      
      """
      solving the puzzle and returning an array of ints, where element 1 of solution_pattern
      is the first rule to apply, and rule n is the last rule
      """
      solution_pattern = self.solve(initial_word, final_word, rules)
      print(solution_pattern)
  
      base_rule = "A_0"
      for rule in solution_pattern:
        base_rule = base_rule + "-" + str(rule)
        button = self.browser.find_element_by_id(base_rule)
        button.click()
        sleep(n)

      next_button = self.browser.find_element_by_id("nextButton")
      next_button.click()
      sleep(n)
      
  def solve(self, init_s, fin_s, rules):

    outputs = [(init_s, "3")]
    ind = 0

    done = False
    while not done:
      current_s = outputs[ind][0]

      if current_s:
        for i in range(3):
          outputs.append((self.apply_rule(current_s, rules[i]), outputs[ind][1] + str(i)))
          if outputs[-1][0] == fin_s:
            done = True
            break
      ind += 1

    rule_pattern = outputs[-1][1][1:]
    to_ret = [int(rule) for rule in rule_pattern]
    return to_ret

  def apply_rule(self, s, rule):
    
    temp = s
    s = s.replace(rule[0], rule[1])
    if s == temp:
      return None
    return s
    
      
      
if __name__=='__main__':
  fss = Formal_System_Solver(URL)
  fss.login()
  fss.play_game()
  #print(fsc.solve("abb", "ccb", [["bb", "ab"], ["bb", "a"], ["a", "c"]]))
