import scrapy
from scrapy import Field


class Person(scrapy.Item):
  id = Field()
  name = Field()
  avatar_url = Field() #头像url
  avatars = Field() # for scrapy image pipline
  avartar_processd = Field()

  headline = Field() #头像签名
  description = Field() #个人简介
  url = Field()
  url_token = Field() #用户名
  gender = Field()
  cover_url = Field()
  type = Field() #账号类型
  badge = Field()
  answer_count = Field() #回答
  articles_count = Field() #赞助的live
  commercial_question_count = Field()
  favorite_count = Field() #收藏数
  favorited_count = Field() #被收藏数
  follower_count = Field() #关注作者的人的数量
  following_columns_count = Field() #作者关注专栏
  following_count = Field() #作者关注他人数量
  pins_count = Field()
  question_count = Field() #提问
  thank_from_count = Field()
  thank_to_count = Field()
  thanked_count = Field() #获得多少次感谢
  vote_from_count = Field()
  vote_to_count = Field()
  voteup_count = Field() #获得多少次赞同
  following_favlists_count = Field() #关注的收藏夹
  following_question_count = Field() #关注的问题
  following_topic_count = Field() #关注的话题
  marked_answers_count = Field()
  mutual_followees_count = Field()
  hosted_live_count = Field() #主持的Live数
  participated_live_count = Field() #参与的live数
  locations = Field()
  educations = Field()
  employments = Field()
