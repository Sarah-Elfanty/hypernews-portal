import json
import random
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View

# Create your views here.
# D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\
with open("D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\news.json", "r") as json_file:
    news_list = json.load(json_file)

print(news_list)
links = [Dict["link"] for Dict in news_list]
print(links)

# creation_dates = set([Dict["created"].split()[0] for Dict in news_list])
# sorted_creation_dates = sorted(creation_dates, reverse=True)
# print(sorted_creation_dates)

class OneNewsPage(View):
    def get(self, request, link_no, *args, **kwargs):
        with open("D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\news.json", "r") as json_file:
            news_list = json.load(json_file)
        # print(link_no)
        links = [Dict["link"] for Dict in news_list]
        if int(link_no) not in links:
            raise Http404
        else:
            news = ""
            for Dict in news_list:
                if int(link_no) in Dict.values():
                    news_title = Dict["title"]
                    date_created = Dict["created"]
                    news_text = Dict["text"]
                    news = "".join(f"""<h2>{news_title}</h2>
                            <p>{date_created}</p>
                            <p>{news_text}</p>
                            <p><a href="/news/" target="_blank"> main page </a><p>""")
            return HttpResponse(f"{news}")


class AllNewsPage(View):

    def SortDates(self, News_List):
        creation_dates = set([Dict["created"].split()[0] for Dict in News_List])
        sorted_creation_dates = sorted(creation_dates, reverse=True)
        return sorted_creation_dates

    def update_list(self, News_list):
        updated_list = []
        for news in news_list:
            Dict = {"created": news["created"].split()[0],
                    "text": news["text"],
                    "title": news["title"],
                    "link": news["link"],
                    }

            updated_list.append(Dict)
        return updated_list


    def get(self, request, *args, **kwargs):

        with open("D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\news.json", "r") as json_file:
            news_list = json.load(json_file)

        q = request.GET.get('q')
        if q:
            found_news = []
            for news in news_list:
                if q in news["title"]:
                    found_news.append(news)
            sorted_dates = self.SortDates(News_List=found_news)
            updated_list = self.update_list(News_list=found_news)
            return render(request, "news/news2.html",
                          context={'sorted_CreationDates': sorted_dates,
                                   'news_list': updated_list, })

        else:
            sorted_dates = self.SortDates(News_List=news_list)
            updated_list = self.update_list(News_list=news_list)
            #return HttpResponse(f'{news_list}')
            return render(request, "news/news2.html",
                          context={'sorted_CreationDates': sorted_dates,
                                   'news_list': updated_list, })


class MainPage(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<p><a href="/news/" target="_blank">News Page</a></p>')


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class CreateNewsPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):

        with open("D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\news.json", "r") as json_file:
            news_list = json.load(json_file)
        links = [Dict["link"] for Dict in news_list]
        created_news = {}
        title = request.POST.get('title')
        text = request.POST.get('title')
        while True:
            link = random.randint(0, 100000)
            if link not in links:
                break
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_news["created"] = created
        created_news["text"] = text
        created_news["title"] = title
        created_news["link"] = link
        news_list.append(created_news)
        with open("D:\\Sarah\\Learning\\HyperNews Portal\\HyperNews Portal\\task\\news.json", "w") as json_file2:
            json.dump(news_list, json_file2)
        return redirect('/news/')
