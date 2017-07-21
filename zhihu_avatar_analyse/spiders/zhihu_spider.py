import scrapy
from scrapy import Request
import json
from zhihu_avatar_analyse.model_person import Person


class ZhihuSpider(scrapy.Spider):
  name = "zhihu"
  allowed_domains = ["www.zhihu.com"]

  startUser = "eisneim"

  URL_USER = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
  QUERY_USER = ("locations,employments,gender,educations,business,"
    "voteup_count,thanked_Count,follower_count,following_count,"
    "cover_url,following_topic_count,following_question_count,"
    "following_favlists_count,following_columns_count,avatar_hue,"
    "answer_count,articles_count,pins_count,question_count,"
    "columns_count,commercial_question_count,favorite_count,"
    "favorited_count,logs_count,marked_answers_count,"
    "marked_answers_text,message_thread_token,account_status,"
    "is_active,is_force_renamed,is_bind_sina,sina_weibo_url,"
    "sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,"
    "is_following,is_followed,mutual_followees_count,vote_to_count,"
    "vote_from_count,thank_to_count,thank_from_count,thanked_count,"
    "description,hosted_live_count,participated_live_count,"
    "allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics")

  URL_FOLLOWER = ("https://www.zhihu.com/api/v4/members/{user}/"
    "followers?include={include}&amp;offset={offset}&amp;limit={limit}")
  QUERY_FOLLOWER = ("data[*].answer_count,articles_count,"
    "gender,follower_count,is_followed,""is_following,"
    "badge[?(type=best_answerer)].topics")

  URL_FOLLOWS = ("https://www.zhihu.com/api/v4/members/{user}/"
    "followees?include={include}&amp;offset={offset}&amp;limit={limit}")
  QUERY_FOLLOWS = ("data[*].answer_count,articles_count,gender,"
    "follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics")

  # start_urls = ["https://www.zhihu.com/people/eisneim/followers"]
  # def __init__(self):
  def start_requests(self):
    yield Request(self.URL_USER.format(user=self.startUser,
      include=self.QUERY_USER), self.parseUser)
    yield Request(self.URL_FOLLOWS.format(user=self.startUser,
      include=self.QUERY_FOLLOWS, offset=0, limit=20), self.parseFollows)
    yield Request(self.URL_FOLLOWER.format(user=self.startUser,
      include=self.QUERY_FOLLOWER, offset=0, limit=20), self.parseFollower)

  def parseUser(self, response):
    result = json.loads(response.text)
    person = Person()
    for field in person.fields:
      if field in result.keys():
        person[field] = result.get(field)
    # special case for avatar
    try:
      avatar_url = result["avatar_url"]
      person["avatars"] = [
        avatar_url,
        avatar_url.replace(
              "_is.jpg", "_xl.jpg").replace("_is.png", "_xl.png"),
        avatar_url.replace(
              "_is.jpg", ".jpg").replace("_is.png", ".png")
      ]
    except:
      print("!!!! >>> fail to save avatar for {}".format(result["url_token"]))

    yield person
    yield Request(self.URL_FOLLOWS.format(user=result.get('url_token'),
      include=self.QUERY_FOLLOWS, offset=0, limit=20), self.parseFollows)
    yield Request(self.URL_FOLLOWER.format(user=result.get('url_token'),
      include=self.QUERY_FOLLOWER, offset=0, limit=20), self.parseFollower)

  def parseFollows(self, response):
    results = json.loads(response.text)
    if "data" in results.keys():
      isPageNotEnd = 'paging' in results.keys() and \
        results.get('paging').get('is_end') == False

      for result in results.get("data"):
        yield Request(self.URL_USER.format(user=result.get('url_token'),
          include=self.QUERY_USER), self.parseUser)
      if isPageNotEnd:
        nextPage = results.get("paging").get("next")
        yield Request(nextPage, self.parseFollows)

  def parseFollower(self, response):
    results = json.loads(response.text)
    if "data" in results.keys():
      for result in results.get("data"):
        yield Request(self.URL_USER.format(user=result.get('url_token'),
          include=self.QUERY_USER), self.parseUser)

      isNextPgaeExits = "paging" in results.keys() and \
        results.get('paging').get('is_end') == False
      if isNextPgaeExits:
        nextPage = results.get("paging").get("next")
        yield Request(nextPage, self.parseFollower)

  # def parse(self, response):
  #   profileSection = response.css(".ProfileHeader-main")
  #   avatarUrl = profileSection.css(
  #     ".ProfileHeader-avatar img::attr(href)").extract_first()
  #   person = {

  #   }
